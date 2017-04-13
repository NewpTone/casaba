#!/bin/bash -ex
# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

export PATH=$PATH:/usr/local/sbin:/usr/sbin

SCENARIO=${SCENARIO:-scenario001}

# We could want to override the default repositories or install behavior
INSTALL_FROM_SOURCE=${INSTALL_FROM_SOURCE:-true}
MANAGE_REPOS=${MANAGE_REPOS:-true}
DELOREAN=${DELOREAN:-http://trunk.rdoproject.org/centos7-master/current-passed-ci/delorean.repo}
DELOREAN_DEPS=${DELOREAN_DEPS:-http://trunk.rdoproject.org/centos7-master/delorean-deps.repo}
GIT_BASE_URL=${GIT_BASE_URL:-git://git.openstack.org}
ADDITIONAL_ARGS=${ADDITIONAL_ARGS:-}
# If logs should be retrieved automatically
COPY_LOGS=${COPY_LOGS:-true}

# Install external Puppet modules with r10k
# Uses the following variables:
#
# - ``GEM_BIN_DIR`` must be set to Gem bin directory
# - ``PUPPETFILE_DIR`` must be set to Puppet modules directory
install_external() {
  $SUDO ${GEM_BIN_DIR}r10k puppetfile install -v --moduledir ${PUPPETFILE_DIR} --puppetfile Puppetfile1
}

# Install Puppet OpenStack modules with zuul-cloner
# Uses the following variables:
#
# - ``PUPPETFILE_DIR`` must be set to Puppet modules directory
# - ``ZUUL_REF`` must be set to Zuul ref. Fallback to 'None'.
# - ``ZUUL_BRANCH`` must be set to Zuul branch. Fallback to 'master'.
# - ``ZUUL_URL`` must be set to Zuul URL
install_openstack() {
  cat > clonemap.yaml <<EOF
clonemap:
  - name: '(.*?)/puppet-(.*)'
    dest: '$PUPPETFILE_DIR/\2'
EOF

  # Periodic jobs run without ref on master
  ZUUL_REF=${ZUUL_REF:-None}
  ZUUL_BRANCH=${ZUUL_BRANCH:-master}

  local project_names=$(awk '{ if ($1 == ":git") print $3 }' \
    Puppetfile0 | tr -d "'," | cut -d '/' -f 4- | xargs
  )
  $SUDO /usr/zuul-env/bin/zuul-cloner -m clonemap.yaml \
    --cache-dir /opt/git \
    --zuul-ref $ZUUL_REF \
    --zuul-branch $ZUUL_BRANCH \
    --zuul-url $ZUUL_URL \
    $GIT_BASE_URL $project_names
}

# Install all Puppet modules with r10k
# Uses the following variables:
#
# - ``GEM_BIN_DIR`` must be set to Gem bin directory
install_all() {
  $SUDO ${GEM_BIN_DIR}r10k puppetfile install -v --puppetfile Puppetfile
}

# Install Puppet OpenStack modules and dependencies by using
# zuul-cloner or r10k.
# Uses the following variables:
#
# - ``PUPPETFILE_DIR`` must be set to Puppet modules directory
# - ``ZUUL_REF`` must be set to Zuul ref
# - ``ZUUL_BRANCH`` must be set to Zuul branch
# - ``ZUUL_URL`` must be set to Zuul URL
install_modules() {
  # If zuul-cloner is there, have it install modules using zuul refs
  if [ -e /usr/zuul-env/bin/zuul-cloner ] ; then
    csplit Puppetfile /'Non-OpenStack modules'/ \
      --prefix Puppetfile \
      --suffix '%d'
    install_external
    install_openstack
  else
    install_all
  fi
  # Copy the Casaba Puppet module
  $SUDO cp -r casaba/puppet/modules/casaba ${PUPPETFILE_DIR}
}

if [ $(id -u) != 0 ]; then
    SUDO='sudo -E'

    # Casaba will connect as root to localhost, set-up the keypair and sshd
    ssh-keygen -t rsa -C "casaba-integration-test" -N "" -f ~/.ssh/id_rsa

    $SUDO mkdir -p /root/.ssh
    cat ~/.ssh/id_rsa.pub | $SUDO tee -a /root/.ssh/authorized_keys
    $SUDO chmod 0600 /root/.ssh/authorized_keys
    $SUDO sed -i 's/^PermitRootLogin no/PermitRootLogin without-password/g' /etc/ssh/sshd_config
    $SUDO service sshd restart
fi

# Sometimes keystone admin port is used as ephemeral port for other connections and gate jobs fail with httpd error 'Address already in use'.
# We reserve port 35357 at the beginning of the job execution to mitigate this issue as much as possible.
# Similar hack is done in devstack https://github.com/openstack-dev/devstack/blob/master/tools/fixup_stuff.sh#L53-L68

# Get any currently reserved ports, strip off leading whitespace
keystone_port=35357
reserved_ports=$(sysctl net.ipv4.ip_local_reserved_ports | awk -F'=' '{print $2;}' | sed 's/^ //')

if [[ -z "${reserved_ports}" ]]; then
    $SUDO sysctl -w net.ipv4.ip_local_reserved_ports=${keystone_port}
else
    $SUDO sysctl -w net.ipv4.ip_local_reserved_ports=${keystone_port},${reserved_ports}
fi

# Make swap configuration consistent
# TODO: REMOVE ME
# https://review.openstack.org/#/c/300122/
source ./tools/fix_disk_layout.sh

# Bump ulimit to avoid too many open file errors
echo "${USER} soft nofile 65536" | $SUDO tee -a /etc/security/limits.conf
echo "${USER} hard nofile 65536" | $SUDO tee -a /etc/security/limits.conf
echo "root soft nofile 65536" | $SUDO tee -a /etc/security/limits.conf
echo "root hard nofile 65536" | $SUDO tee -a /etc/security/limits.conf

# Setup repositories
if [ "${MANAGE_REPOS}" = true ]; then
    $SUDO curl -L ${DELOREAN} -o /etc/yum.repos.d/delorean.repo
    $SUDO curl -L ${DELOREAN_DEPS} -o /etc/yum.repos.d/delorean-deps.repo
    $SUDO yum update -y
fi

# Install dependencies
$SUDO yum -y install puppet \
                     yum-plugin-priorities \
                     iproute \
                     dstat \
                     python-setuptools \
                     openssl-devel \
                     python-devel \
                     libffi-devel \
                     libxml2-devel \
                     libxslt-devel \
                     libyaml-devel \
                     ruby-devel \
                     openstack-selinux \
                     policycoreutils \
                     rubygems \
                     wget \
                     "@Development Tools"

# Don't assume pip is installed
which pip || $SUDO easy_install pip

# Try to use pre-cached cirros images, if available, otherwise download them
rm -rf /tmp/cirros
mkdir /tmp/cirros

if [ -f ~/cache/files/cirros-0.3.4-x86_64-uec.tar.gz ]; then
    tar -xzvf ~/cache/files/cirros-0.3.4-x86_64-uec.tar.gz -C /tmp/cirros/
else
    echo "No pre-cached uec archive found, downloading..."
    wget --tries=10 http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-uec.tar.gz -P /tmp/cirros/
    tar -xzvf /tmp/cirros/cirros-0.3.4-x86_64-uec.tar.gz -C /tmp/cirros/
fi
if [ -f ~/cache/files/cirros-0.3.4-x86_64-disk.img ]; then
    cp -p ~/cache/files/cirros-0.3.4-x86_64-disk.img /tmp/cirros/
else
    echo "No pre-cached disk image found, downloading..."
    wget --tries=10 http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img -P /tmp/cirros/
fi
echo "Using pre-cached images:"
find /tmp/cirros -type f -printf "%m %n %u %g %s  %t" -exec md5sum \{\} \;

# TO-DO: Casaba should handle Hiera and Puppet configuration, so that it works
# no matter the environment
$SUDO su -c 'cat > /etc/puppet/puppet.conf <<EOF
[main]
    logdir = /var/log/puppet
    rundir = /var/run/puppet
    ssldir = $vardir/ssl
    hiera_config = /etc/puppet/hiera.yaml

[agent]
    classfile = $vardir/classes.txt
    localconfig = $vardir/localconfig
EOF'
$SUDO su -c 'cat > /etc/puppet/hiera.yaml <<EOF
---
:backends:
  - yaml
:yaml:
  :datadir: /placeholder
:hierarchy:
  - common
  - defaults
  - "%{clientcert}"
  - "%{environment}"
  - global
EOF'

# To make sure wrong config files are not used
if [ -d /home/jenkins/.puppet ]; then
  $SUDO rm -f /home/jenkins/.puppet
fi
$SUDO puppet config set hiera_config /etc/puppet/hiera.yaml

# Setup dstat for resource usage tracing
if type "dstat" 2>/dev/null; then
  $SUDO dstat -tcmndrylpg \
              --top-cpu-adv \
              --top-io-adv \
              --nocolor | $SUDO tee -a /var/log/dstat.log > /dev/null &
fi

# Setup casaba
if [ "${INSTALL_FROM_SOURCE}" = true ]; then
  $SUDO pip install .
  export GEM_BIN_DIR=/tmp/casabagems/bin/
  export PUPPETFILE_DIR=/usr/share/openstack-puppet/modules
  export GEM_HOME=/tmp/casabagems
  $SUDO gem install r10k --no-ri --no-rdoc
  # make sure there is no puppet module pre-installed
  $SUDO rm -rf "${PUPPETFILE_DIR:?}/"*
  install_modules
else
  $SUDO yum -y install openstack-casaba
fi

# Make sure there are no other puppet modules in the system (happens in gate)
$SUDO rm -rf /etc/puppet/modules/*

# Make sure the fqdn is associated to the IP in /etc/hosts
# Needed for Horizon SSL tests in Tempest
echo -e "\n127.0.0.1 $(facter fqdn)" | $SUDO tee -a /etc/hosts

# Generate configuration from selected scenario and run it
source ./tests/${SCENARIO}.sh
result=$?

# Print output and generate subunit if results exist
if [ -d /var/lib/tempest ]; then
    pushd /var/lib/tempest
    $SUDO /usr/bin/testr last || true
    $SUDO bash -c "/usr/bin/testr last --subunit > /var/tmp/casaba/latest/testrepository.subunit" || true
    popd
fi

if [ "${COPY_LOGS}" = true ]; then
    source ./tools/copy-logs.sh
    recover_default_logs
fi

if [ "${FAILURE}" = true ]; then
    exit 1
fi

exit $result
