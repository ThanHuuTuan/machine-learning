#!/usr/bin/python

## @data_validator.py
#  This script performs various data sanitation on input data, and 
#  validates the same data to ensure that the SVM algorithm will work
#  on the given dataset.  This adds an extra layer of security,
#  especially if the script later is used without a web interface.
import json, sys, magic
from jsonschema import validate
from helper import md5_for_file
from jsonschema_definition import jsonschema_training, jsonschema_analysis, jsonschema_dataset, jsonschema_dataset_id

## Class: Validator
class Validator:

  ## constructor: saves a subset of the passed-in form data
  #
  #  @svm_data    : is the input data, generally a form POST data, if
  #                 the 'session_type' is training.
  #  @session_type: represents the current session type
  def __init__(self, svm_data=None, session_type=None):
    self.svm_data    = svm_data
    self.svm_session = json.loads(self.svm_data)['data']['settings']['svm_session'].lower()

  ## data_validation: this method validates the SVM properties of either
  #                   'training', or 'analysis' sessions.
  #
  #  Note: This method does not validate the associated 'file upload(s)'. The
  #        latter component is validated via 'file_upload_validation', and 
  #        'dataset_validation' methods (see below).
  def data_validation(self):
    # local variables
    flag_json  = False
    list_error = []

    # determine if input data is a JSON object
    try:
      json_data = json.loads(self.svm_data)['data']['settings']
      flag_json = True
    except ValueError, e:
      error     = 'The SVM settings have not been properly configured'
      list_error.append(error)
      flag_json = False

    # validation on 'data_new' session
    if self.svm_session == 'data_new' and flag_json:
      try:
        validate(json.loads(self.svm_data)['data']['settings'], jsonschema_training())
      except Exception, error:
        list_error.append(str(error))

      # validation on 'xml file(s)'
      if ( json_data.get('svm_dataset_type', None) == 'upload file' and json_data.get('svm_dataset', None) ):
        for index, xmldata in enumerate(json_data['svm_dataset']):
          print xmldata

    # validation on 'data_append' session

    # validation on 'model_generate' session

    # validation on 'model_use' session
    elif self.svm_session == 'model_use' and flag_json:
      try:
        validate(json.loads(self.svm_data)['data']['settings'], jsonschema_analysis())
      except Exception, error:
        list_error.append(str(error))

    # return error
    if len(list_error) > 0:
      return { 'status': False, 'error': list_error }
    else:
      return { 'status': True, 'error': None }

  ## dataset_validation: each supplied SVM dataset is correctly formatted via corresponding
  #                      methods in 'svm_json.py'. After being formatted, each dataset is
  #                      validated in this method.
  #
  #  Note: the SVM dataset is synonymous for the 'file upload(s)'
  def dataset_validation(self):
    # local variables
    list_error = []

    # iterate outer dict
    for key, value in self.svm_data.iteritems():
      try:
        if key == 'svm_dataset':
          for dict in value:
            try:
              validate( dict, jsonschema_dataset() )
            except Exception, error:
              list_error.append(str(error))
        elif key == 'id_entity':
          try:
            validate( {key: value}, jsonschema_dataset_id() )
          except Exception, error:
            list_error.append(str(error))
      except Exception, error:
        list_error.append(str(error))

    # return error
    if len(list_error) > 0:
      return { 'status': False, 'error': list_error }
    else:
      return { 'status': True, 'error': None }

  ## file_upload_validation: this method validates the MIME type of 'file upload(s)',
  #                          provided during a 'training' session. If any of the 'file
  #                          upload(s)' fails validation, this method will return False.
  #                          Otherwise, the method will return a list of unique 'file
  #                          upload(s)', discarding duplicates.
  def file_upload_validation(self, json_file_obj):
    # local variables
    list_error       = []

    json_data        = json.loads(json_file_obj)['data']['dataset']
    acceptable_type  = ['text/plain', 'text/csv', 'application/xml']

    unique_hash      = set()
    json_keep        = []

    if (json_data.get('file_upload', None)):

      for index, filedata in enumerate(json_data['file_upload']):
        try:
          mimetype = magic.from_file( filedata['file_temp'][0], mime=True )
          # validate file format
          if ( mimetype not in acceptable_type ):
            msg =  '''Problem: Uploaded file, \'''' + filedata['file_temp'][0] + '''\', must be one of the formats:'''
            msg += '\n       ' + ', '.join(acceptable_type)
            list_error.append(msg)

          filehash = md5_for_file(filedata['file_temp'][0])
          # add 'hashed' value of file reference(s) to a list
          if filehash not in unique_hash:
            unique_hash.add(filehash)
            json_keep.append( {'type': mimetype, 'filedata': filedata} )

        except:
          msg = 'Problem with file upload #' + str(index) + '. Please re-upload the file.'
          list_error.append(msg)

      # replace portion of JSON with unique 'file reference(s)'
      json_data['file_upload'][:] = json_keep

    else:
      msg = 'No file(s) were uploaded'
      list_error.append(msg)

    # return error
    if len(list_error) > 0:
      return { 'status': False, 'error': list_error, 'json_data': None }
    else:
      return { 'status': True, 'error': None, 'json_data': json_data }
