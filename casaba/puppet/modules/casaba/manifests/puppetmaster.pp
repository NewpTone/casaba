#   This class is used to install puppetmaster node.
class casaba::puppetmaster (
  # Firewall
  $enable_firewall        = true,
  # puppetmaster
  $enable_ha              = false,
  $foreman_url            = '',
  $storeconfigs_backend   = 'puppetdb',
  $puppet_port            = '8140',
  $puppet_dbpassword      = 'puppet',
  # puppetdb
  $enable_puppetdb        = false,
  $puppetdb_server        = $::fqdn,
){

  # Configure puppet-server
  class { '::puppet::server':
    enable_ha            => $enable_ha,
    foreman_url          => $foreman_url,
    storeconfigs_backend => $storeconfigs_backend,
    port                 => $puppet_port,
    dbpassword           => $puppet_dbpassword,
    dbserver             => $db_host,
  }

  if $enable_puppetdb {
    class { '::puppetdb::master::config':
      puppetdb_server             => $puppetdb_server,
      restart_puppet              => false,
      strict_validation           => false,
      puppetdb_soft_write_failure => true
    }
  }
}
