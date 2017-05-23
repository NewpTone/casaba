# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Plugin responsible for setting OpenStack global options
"""

import os
import uuid

from casaba.installer import basedefs
from casaba.installer import exceptions
from casaba.installer import processors
from casaba.installer import utils
from casaba.installer import validators

from casaba.modules.common import is_all_in_one
from casaba.modules.documentation import update_params_usage

# ------------- Prescript Casaba Plugin Initialization --------------

PLUGIN_NAME = "Prescript"
PLUGIN_NAME_COLORED = utils.color_text(PLUGIN_NAME, 'blue')


def initConfig(controller):

    params = {
        "GLOBAL": [

            {"CMD_OPTION": "default-password",
             "PROMPT": (
                 "Set the default value of password"
                 ""
             ),
             "OPTION_LIST": [],
             "DEFAULT_VALUE": '',
             "MASK_INPUT": True,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_DEFAULT_PASSWORD",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": True,
             "CONDITION": False},

            {"CMD_OPTION": "service-workers",
             "PROMPT": (
                 "Set the workers of service"
             ),
             "OPTION_LIST": [],
             "DEFAULT_VALUE": '%{::processorcount}',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_SERVICE_WORKERS",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "config-package-version",
             "PROMPT": "whether configure package version",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_PACKAGE_VERSION",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "environment",
             "PROMPT": "Set the environment of cluster",
             "OPTION_LIST": ["development", "test", "production"],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "production",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_ENVIRONMENT",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "domain_name",
             "PROMPT": "Set domain name of cluster",
             "OPTION_LIST": [],
             "VALIDATORS": [validators.validate_not_empty],
             "DEFAULT_VALUE": '0.example.domain.in',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_DOMAIN_NAME",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},


            {"CMD_OPTION": "separate_network",
             "PROMPT": "Separate network service from controller",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": 'n',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_SEPARATE_NETWORK",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "manage_prefix",
             "PROMPT": "manage ipaddress prefix",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "DEFAULT_VALUE": '192.168.1.',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_MANAGE_PREFIX",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "storage_prefix",
             "PROMPT": "Set storage prefix",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "DEFAULT_VALUE": '192.168.2.',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_STORAGE_PREFIX",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "sdn_prefix",
             "PROMPT": "Set SDN network prefix",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "DEFAULT_VALUE": '192.168.3.',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_SDN_PREFIX",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "enable_galera",
             "PROMPT": "Whether enable Galera service",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": 'n',
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": True,
             "CONF_NAME": "CONFIG_ENABLE_GALERA",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-glance-install",
             "PROMPT": (
                 "Install OpenStack Image Service (Glance)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_GLANCE_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-cinder-install",
             "PROMPT": (
                 "InstallOpenStack Block Storage (Cinder)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_CINDER_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-gringotts-install",
             "PROMPT": (
                 "InstallPoleX OS Billing (Gringotts)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_GRINGOTTS_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-manila-install",
             "PROMPT": (
                 "InstallOpenStack Shared File System "
                 "(Manila)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_MANILA_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-nova-install",
             "PROMPT": (
                 "InstallOpenStack Compute (Nova)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_NOVA_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-neutron-install",
             "PROMPT": (
                 "InstallOpenStack Networking (Neutron)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_NEUTRON_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-horizon-install",
             "PROMPT": (
                 "Install OpenStack Dashboard (Horizon)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_HORIZON_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-swift-install",
             "PROMPT": (
                 "Install OpenStack Object Storage (Swift)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_SWIFT_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-ceilometer-install",
             "PROMPT": (
                 "Install OpenStack Metering (Ceilometer)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_CEILOMETER_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-aodh-install",
             "PROMPT": (
                 "Install OpenStack Telemetry Alarming (Aodh)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_AODH_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-gnocchi-install",
             "PROMPT": (
                 "Install OpenStack Resource Metering (Gnocchi)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_GNOCCHI_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-panko-install",
             "PROMPT": (
                 "Install OpenStack Events Service (Panko)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_PANKO_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-sahara-install",
             "PROMPT": (
                 "Install OpenStack Clustering (Sahara)."
                 " If yes it'll also install Heat."
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_SAHARA_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-heat-install",
             "PROMPT": (
                 "Install OpenStack Orchestration (Heat)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_HEAT_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-magnum-install",
             "PROMPT": (
                 "Install OpenStack Container Infrastructure Management Service (Magnum)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_MAGNUM_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-trove-install",
             "PROMPT": (
                 "InstallOpenStack Database (Trove)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_TROVE_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-ironic-install",
             "PROMPT": (
                 "InstallOpenStack Bare Metal (Ironic)"
             ),
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_IRONIC_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-client-install",
             "PROMPT": "Install OpenStack client tools",
             "OPTION_LIST": ["y", "n"],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "y",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_CLIENT_INSTALL",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-debug-mode",
             "PROMPT": "Do you want to run OpenStack services in debug mode",
             "OPTION_LIST": ["y", "n"],
             "DEFAULT_VALUE": "n",
             "VALIDATORS": [validators.validate_options],
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_DEBUG_MODE",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "os-controller-host",
             "PROMPT": "Enter controller host",
             "OPTION_LIST": [],
             "VALIDATORS": [validators.validate_ssh],
             "DEFAULT_VALUE": utils.get_localhost_ip(),
             "CONF_NAME": "CONFIG_CONTROLLER_HOST",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CONF_NAME": "CONFIG_COMPUTE_HOSTS",
             "CMD_OPTION": "os-compute-hosts",
             "PROMPT": "Enter compute host",
             "OPTION_LIST": [],
             "VALIDATORS": [validators.validate_multi_ssh],
             "DEFAULT_VALUE": utils.get_localhost_ip(),
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False,
             },

            {"CMD_OPTION": "os-network-hosts",
             "PROMPT": "Enter network host",
             "OPTION_LIST": [],
             "VALIDATORS": [validators.validate_multi_ssh],
             "DEFAULT_VALUE": utils.get_localhost_ip(),
             "CONF_NAME": "CONFIG_NETWORK_HOSTS",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False,
             },

            {"CMD_OPTION": "use-subnets",
             "PROMPT": ("Should interface names be automatically recognized "
                        "based on subnet CIDR"),
             "OPTION_LIST": ['y', 'n'],
             "VALIDATORS": [validators.validate_options],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "LOOSE_VALIDATION": False,
             "CONF_NAME": "CONFIG_USE_SUBNETS",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "enable-repo",
             "PROMPT": ("Enter a comma separated list of URLs to "
                        "yum repositories to install"),
             "OPTION_LIST": ['y', 'n'],
             "VALIDATORS": [validators.validate_not_empty],
             "PROCESSORS": [processors.process_bool],
             "DEFAULT_VALUE": "n",
             "MASK_INPUT": False,
             "CONF_NAME": "CONFIG_REPO",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},

            {"CMD_OPTION": "enable-dev-mode",
             "PROMPT": ("This option only for casaba developers"
                        "to use"),
             "OPTION_LIST": ['none', 'git', 'rpm'],
             "VALIDATORS": [validators.validate_not_empty],
             "DEFAULT_VALUE": "rpm",
             "MASK_INPUT": False,
             "CONF_NAME": "CONFIG_DEV_MODE",
             "USE_DEFAULT": False,
             "NEED_CONFIRM": False,
             "CONDITION": False},
        ],
    }
    update_params_usage(basedefs.CASABA_DOC, params)

    groups = [
        {"GROUP_NAME": "GLOBAL",
         "DESCRIPTION": "Global Options",
         "PRE_CONDITION": lambda x: 'yes',
         "PRE_CONDITION_MATCH": "yes",
         "POST_CONDITION": False,
         "POST_CONDITION_MATCH": True},
    ]

    config = controller.CONF

    for group in groups:
        controller.addGroup(group, params[group['GROUP_NAME']])


def initSequences(controller):
    prescript_steps = [
        {'title': 'Preparing Global Parameters Settings',
         'functions': [deploy_prep]},
        {'title': 'Preparing Operating System settings',
         'functions': [preinstall_and_discover]},
    ]

    controller.addSequence("Running pre configuration scripts", [], [],
                           prescript_steps)

# ------------------------- helper functions -------------------------


def manage_rdo_repo(config):
    """
    Installs and enables RDO repo on host in case it is installed locally.
    """
    try:
        cmd = "rpm -q rdo-release --qf='%{version}-%{release}.%{arch}\n'"
        rc, out = utils.execute(cmd, use_shell=True)
    except exceptions.ExecuteRuntimeError:
        # RDO repo is not installed, so we don't need to continue
        return

    match = re.match(r'^(?P<version>\w+)\-(?P<release>\d+\.[\d\w]+)\n', out)
    version, release = match.group('version'), match.group('release')
    rdo_url = ("https://www.rdoproject.org/repos/openstack-%(version)s/"
               "rdo-release-%(version)s.rpm" % locals())

    server = utils.ScriptRunner()
    server.append("(rpm -q 'rdo-release-%(version)s' ||"
                  " yum install -y --nogpg %(rdo_url)s) || true"
                  % locals())
    try:
        server.execute()
    except exceptions.ScriptRuntimeError as ex:
        msg = ('Failed to set RDO repo :\n%s'
               % (ex))
        raise exceptions.ScriptRuntimeError(msg)
# -------------------------- step functions --------------------------


def preinstall_and_discover(config, messages):
    """Installs Puppet and it's dependencies and dependencies of Puppet
    modules' package and discovers information about all hosts.
    """
    details = {}
    # Step 1 enable PoleX repo
    if config['CONFIG_REPO']:
        manage_polex_repo(config)

    server = utils.ScriptRunner()
    # Step 2 install Puppet and it's dependencies
    if config['CONFIG_REPO']:

        if is_all_in_one(config):
            deps = list(basedefs.PUPPET_DEPENDENCIES) + list(basedefs.PUPPET_MODULES_DEPS) + list(basedefs.DEVELOP_DEPS)
        else:
            deps = list(basedefs.PUPPET_DEPENDENCIES)

        packages = ' '.join(deps)
        server.append('timeout 60 yum install -y %s' % packages)
        # yum does not fail if one of the packages is missing
        for package in deps:
            server.append('rpm -q --whatprovides %s' % package)
        server.execute()
        server.clear()

    server.append('mkdir -p %s' % basedefs.CASABA_VAR_DIR)
    # Separately create the tmp directory for this packstack run, this will
    # fail if the directory already exists
    host_dir = os.path.join(basedefs.CASABA_VAR_DIR, uuid.uuid4().hex)
    server.append('mkdir --mode 0700 %s' % host_dir)
    for i in ('modules', 'resources'):
        server.append('mkdir --mode 0700 %s' % os.path.join(host_dir, i))
    server.execute()
    details['tmpdir'] = host_dir

    # discover other host info; Facter is installed as Puppet dependency,
    # so we let it do the work
    server.clear()
    server.append('facter -p')
    rc, stdout = server.execute()
    for line in stdout.split('\n'):
        try:
            key, value = line.split('=>', 1)
        except ValueError:
            # this line is probably some warning, so let's skip it
            continue
        else:
            details[key.strip()] = value.strip()
    server.clear()
    config['HOST_DETAILS'] = details


def deploy_prep(config, messages):

    server = utils.ScriptRunner()
    server.append('rpm -q --whatprovides yum-utils || '
                  'yum install -y yum-utils')
    server.execute()

    # generateHieraDataDir(config['CONFIG_ENVIRONMENT'], config['CONFIG_DOMAIN_NAME'])

    # Do some params prescript
    config['CONFIG_CLUSTER_MEMBERS'] = [f.strip() for f in config['CONFIG_CLUSTER_MEMBERS'].split(',')]
    # We need to process the CONFIG_CONTROLLER_HOST, it could be str or list.
    if type(config['CONFIG_CONTROLLER_HOST']) is str:
        config['CONFIG_CONTROLLER_HOST'] = config['CONFIG_CONTROLLER_HOST'].split(',')

    config['CONFIG_LB_HOST'] = 'lb.' + config['CONFIG_DOMAIN_NAME']
