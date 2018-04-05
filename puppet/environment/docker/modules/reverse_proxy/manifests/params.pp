###
### params.pp: default class parameters.
###
### @members, corresponds to an existing webserver.
###
class reverse_proxy::params {
    $hiera = lookup( { 'name' => 'reverse_proxy', 'default_value' => false } )

    if $hiera {
        $run            = true
        $version        = 'latest'
        $type           = $hiera['type']
        $vhost          = $hiera['vhost']
        $host_port      = $hiera['host_port']
        $listen_port    = $hiera['listen_port']
        $members        = $hiera['members']
        $proxy          = $hiera['proxy']
        $self_signed    = true
        $cert_path      = $hiera['certificate']['cert_path']
        $pkey_path      = $hiera['certificate']['pkey_path']
        $cert_country   = $hiera['certificate']['props']['country']
        $cert_org       = $hiera['certificate']['props']['org']
        $cert_state     = $hiera['certificate']['props']['state']
        $cert_locality  = $hiera['certificate']['props']['locality']
        $cert_unit      = $hiera['certificate']['props']['unit']
        $cert_bit       = $hiera['certificate']['props']['bit']
        $cert_days      = $hiera['certificate']['props']['days']
        $access_log     = $hiera['access_log']
        $error_log      = $hiera['error_log']
    }

    else {
        $run            = true
        $version        = $nginx_version
        $type           = ''
        $vhost          = ''
        $host_port      = ''
        $listen_port    = ''
        $members        = ['']
        $proxy          = 'http://localhost'
        $self_signed    = true
        $cert_path      = '/etc/puppetlabs/puppet/ssl/certs'
        $pkey_path      = '/etc/puppetlabs/puppet/ssl/private_keys'
        $cert_country   = ''
        $cert_org       = ''
        $cert_state     = ''
        $cert_locality  = ''
        $cert_unit      = ''
        $cert_bit       = 4096
        $cert_days      = 365
        $access_log     = '/var/log/nginx/puppet_access.log'
        $error_log      = '/var/log/nginx/puppet_error.log'
    }
}
