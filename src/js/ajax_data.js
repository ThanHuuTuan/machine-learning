/**
 * ajax_data.js: this script utilizes ajax to relay the form POST data, specifically,
 *               'file uploads' to a defined 'action' script.
 *
 * Note: the implemented AJAX methods, and properties, are discussed more fully within
 *       'ajax_json.js'
 */

$(document).ready(function() {
  $('form').on('submit', function(event) {
    event.preventDefault();

  // local variables
    var arr_data = new Array();

  // store 'file uploads' in array
    var dataset = $('input[name="svm_dataset[]"]');
    if ( dataset.length > 0 && dataset.attr('type') == 'file' ) {
      $( dataset ).each(function( index ) {
        arr_data.push( dataset.eq(index).prop('files'));
      });
      console.log(arr_data);
    }

  // ajax request: 'svm_dataset[]' file upload(s)
    $.ajax({
      url: '../../php/dataset.php',
      type: 'POST',
      data: dataset_array
    }).done(function(data) {
      console.log('Success: data upload');
    }).fail(function(jqXHR, textStatus, errorThrown) {
      console.log('Fail: data upload');
    });

  });
});
