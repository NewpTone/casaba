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
Installs and configures OpenStack Xxx
"""

import os

from casaba.installer import basedefs
from casaba.installer import utils
from casaba.installer import validators
from casaba.installer import processors

from casaba.modules.documentation import update_params_usage
from casaba.modules.ospluginutils import generateHieraDataFile
from casaba.modules.ospluginutils import generateHieraDataDir
from casaba.modules.sorteddict import UnsortableOrderedDict

# ------------- Xxx Casaba Plugin Initialization --------------

PLUGIN_NAME = "Xxx"
PLUGIN_NAME_COLORED = utils.color_text(PLUGIN_NAME, 'blue')


def initConfig(controller):
    params = [
        {"CMD_OPTION": "xxxx_option",
         "PROMPT": "xxxx description",
         "OPTION_LIST": [],
         "VALIDATORS": [validators.validate_not_empty],
         "DEFAULT_VALUE": 'xxxx',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_xxx_option",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "yes-or-no",
         "PROMPT": "enable xxx service",
         "OPTION_LIST": ['y', 'n'],
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_bool],
         "DEFAULT_VALUE": 'y',
         "MASK_INPUT": False,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_ENABLE_xxx",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": False,
         "CONDITION": False},

        {"CMD_OPTION": "xx-password",
         "PROMPT": "set xx password",
         "OPTION_LIST": '',
         "VALIDATORS": [validators.validate_not_empty],
         "PROCESSORS": [processors.process_password],
         "DEFAULT_VALUE": "PW_PLACEHOLDER",
         "MASK_INPUT": True,
         "LOOSE_VALIDATION": False,
         "CONF_NAME": "CONFIG_xx",
         "USE_DEFAULT": False,
         "NEED_CONFIRM": True,
         "CONDITION": False},

    ]
    update_params_usage(basedefs.CASABA_DOC, params, sectioned=False)
    group = {"GROUP_NAME": "xxxx",
             "DESCRIPTION": "Polex xxxx Config parameters",
             "PRE_CONDITION": False,
             "PRE_CONDITION_MATCH": True,
             "POST_CONDITION": False,
             "POST_CONDITION_MATCH": True}
    controller.addGroup(group, params)


def initSequences(controller):

    steps = [
        {'title': 'Preparing Xxx entries',
         'functions': [create_hieradata]}
    ]
    controller.addSequence("Configuring Xxx", [], [], steps)


# -------------------------- step functions --------------------------

def create_hieradata(config, message):

    xxxx_options = UnsortableOrderedDict()

    xxxx_options['key1'] = config['CONFIG_XXX']

    _, HIERA_COMMON_DIR = generateHieraDataDir(config['CONFIG_ENVIRONMENT'],
                          config['CONFIG_DOMAIN_NAME'])
    hiera_file = os.path.join(HIERA_COMMON_DIR, 'xxx.yaml')
    generateHieraDataFile(hiera_file, xxxx_options)
