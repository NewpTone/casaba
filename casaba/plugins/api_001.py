# -*- coding: utf-8 -*-
#
# Author: Xingchao Yu <yuxcer@gmail.com>
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
Installs and configures OpenStack API
"""

from casaba.installer import basedefs
from casaba.installer import utils
from casaba.installer import validators
from casaba.installer import processors

from casaba.modules.documentation import update_params_usage

# ------------- API Plugin Initialization --------------

PLUGIN_NAME = "API"
PLUGIN_NAME_COLORED = utils.color_text(PLUGIN_NAME, 'blue')


def initConfig(controller):
    params = [
        {"CMD_OPTION": "ceph_monitor_host",
         "PROMPT": "Setup address of ceph monitor",
         "OPTION_LIST": [],
         "VALIDATORS": [validators.validate_not_empty],
         "DEFAULT_VALUE": '127.0.0.1',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_MONITOR_HOST",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "memcache_servers",
         "PROMPT": "Setup address of memcache server",
         "OPTION_LIST": [],
         "VALIDATORS": [validators.validate_not_empty],
         "DEFAULT_VALUE": '127.0.0.1:11211',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_MEMCACHE_SERVERS",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "enable_install_api",
         "PROMPT": "Whether or not to enable OpenStack API service",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'y',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_ENABLE_INSTALL_API",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "enable_vpn_agent",
         "PROMPT": "Whether or not to enable VPN Agent",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'y',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_ENABLE_VPN_AGENT",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "enable_fwaas_agent",
         "PROMPT": "Whether or not to enable FWaaS Agent",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'y',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_ENABLE_FWAAS_AGENT",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "enable_lbaas_agent",
         "PROMPT": "Whether or not to enable LBaaS Agent",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'y',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_ENABLE_LBAAS_AGENT",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "os_debug",
         "PROMPT": "enable OpenStack service debug mode",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'n',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_OS_DEBUG",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "use_syslog",
         "PROMPT": "use syslog for OpenStack",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'n',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_USE_SYSLOG",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},
    ]
    update_params_usage(basedefs.casaba_DOC, params, sectioned=False)
    group = {"GROUP_NAME": "API",
             "DESCRIPTION": "OpenStack API Node Config parameters",
             "PRE_CONDITION": False,
             "PRE_CONDITION_MATCH": True,
             "POST_CONDITION": False,
             "POST_CONDITION_MATCH": True}
    controller.addGroup(group, params)


def initSequences(controller):

    steps = [
        {'title': 'Preparing API entries',
         'functions': [create_hieradata]}
    ]
    controller.addSequence("Configuring API", [], [], steps)


# -------------------------- step functions --------------------------

def create_hieradata(config, message):

    if len(config['CONFIG_CONTROLLER_HOST']) == 3:
        basedefs.API_GLOBAL_OPTIONS['sunfire::controller::enable_install_api'] = config['CONFIG_ENABLE_INSTALL_API']
        basedefs.API_GLOBAL_OPTIONS['sunfire::controller::cluster_members'] = config['CONFIG_CLUSTER_MEMBERS']
        basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_ha'] = True
    else:
        basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_install_api'] = config['CONFIG_ENABLE_INSTALL_API']
        basedefs.API_GLOBAL_OPTIONS['sunfire::api::cluster_members'] = config['CONFIG_CLUSTER_MEMBERS']
        basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_ha'] = False

    basedefs.API_GLOBAL_OPTIONS['sunfire::storage::ceph::client::mon_hosts'] = config['CONFIG_MONITOR_HOST']
    basedefs.API_GLOBAL_OPTIONS['sunfire::openstack::neutron_controller::enable_vpn_agent'] = config['CONFIG_ENABLE_VPN_AGENT']
    basedefs.API_GLOBAL_OPTIONS['sunfire::openstack::neutron_network::enable_fwaas_agent'] = config['CONFIG_ENABLE_FWAAS_AGENT']
    basedefs.API_GLOBAL_OPTIONS['sunfire::openstack::neutron_network::enable_lbaas_agent'] = config['CONFIG_ENABLE_LBAAS_AGENT']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_horizon'] = config['CONFIG_HORIZON_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_heat'] = config['CONFIG_HEAT_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_gnocchi'] = config['CONFIG_GNOCCHI_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_aodh'] = config['CONFIG_AODH_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_ceilometer'] = config['CONFIG_CEILOMETER_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_ceilometer_central'] = config['CONFIG_CEILOMETER_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_swift'] = config['CONFIG_SWIFT_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_trove'] = config['CONFIG_TROVE_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_nova'] = config['CONFIG_NOVA_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_glance'] = config['CONFIG_GLANCE_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_cinder'] = config['CONFIG_CINDER_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_cinder_volume'] = config['CONFIG_CINDER_INSTALL']
    basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_neutron'] = config['CONFIG_NEUTRON_INSTALL']
    config['CONFIG_MEMCACHE_SERVERS'] = processors.change_str_to_list(config['CONFIG_MEMCACHE_SERVERS'])
    # Enable systemd ha
    if len(config['CONFIG_CONTROLLER_HOST']) == 3:
        basedefs.API_GLOBAL_OPTIONS['sunfire::api::enable_systemd_ha'] = True
