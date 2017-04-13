# Casaba Overview

**Casaba** is a utility to install **OpenStack** on **Red Hat** based operating system.
**Casaba** is originally forked from **Packstack**, but it use Puppet C/S mode to take
place of standalone mode.
Besides that, it not only used for POC environment, but also for deploying OpenStack
production environment with dedicated design.

This utility is still in the early stages, a lot of the services and functions need
to be added.

## Installation of casaba:

    $ yum install -y git
    $ git clone git://github.com/openstack/casaba.git
    $ cd casaba && sudo python setup.py install

## Installation of openstack-puppet-modules (REQUIRED if running casaba from source):

    $ export GEM_HOME=/tmp/somedir
    $ gem install r10k
    $ sudo -E /tmp/somedir/bin/r10k puppetfile install -v
    $ sudo cp -r casaba/puppet/modules/casaba /usr/share/openstack-puppet/modules

### Option 1 (all-in-one)

    $ casaba --allinone

This will install all **OpenStack** services on a single host without
prompting for any configuration information.  This will generate an
"answers" file (`casaba-answers-<date>-<time>.txt`) containing all
the values used for the install.

If you need to re-run casaba, you must use the `--answer-file`
option in order for casaba to use the correct values for passwords
and other authentication credentials:

    $ casaba --answer-file casaba-answers-<date>-<time>.txt

### Option 2 (using answer file)

    $ casaba --gen-answer-file=ans.txt

Then edit `ans.txt` as appropriate e.g.

- set `CONFIG_SSH_KEY` to a public ssh key to be installed to remote machines
- Edit the IP address to anywhere you want to install a piece of OpenStack on another server
- Edit the 3 network interfaces to whatever makes sense in your setup

you'll need to use a icehouse repository for example for RHEL

    $ CONFIG_REPO=http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/epel-6/

    $ casaba --answer-file=ans.txt

### Option 3 (prompts for configuration options)

    $ casaba

that's it, if everything went well you can now start using OpenStack

    $ cd
    $ . keystonerc_admin
    $ nova list
    $ swift list  # if you have installed swift

## Config options

- `CONFIG_NOVA_COMPUTE_HOSTS` :
  * A comma separated list of ip addresses on which to install nova compute
- `CONFIG_SWIFT_STORAGE_HOSTS` :
  * A comma separated list of swift storage devices
    * `1.1.1.1`: create a testing loopback device and use this for storage
    * `1.1.1.1/sdb`: use `/dev/sdb` on `1.1.1.1` as a storage device

## Logging

The location of the log files and generated puppet manifests are in the
`/var/tmp/casaba` directory under a directory named by the date in which
**Casaba** was run and a random string (e.g. `/var/tmp/casaba/20131022-204316-Bf3Ek2`).
Inside, we find a manifest directory and the `openstack-setup.log` file; puppet
manifests and a log file for each one are found inside the manifest directory.

## Debugging

To make **Casaba** write more detailed information into the log file you can use the `-d` switch:

    $ casaba -d --allinone
