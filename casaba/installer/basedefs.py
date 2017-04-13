# -*- coding: utf-8 -*-
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
This module provides all the predefined variables.
"""

import datetime
import os
import pkg_resources
import sys
import tempfile

from .utils import get_current_user
from casaba.modules.sorteddict import UnsortableOrderedDict


APP_NAME = "Casaba"

FILE_YUM_VERSION_LOCK = "/etc/yum/pluginconf.d/versionlock.list"

CASABA_SRC_DOC = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse('casaba'), 'docs/casaba.rst'
)
if os.path.exists(CASABA_SRC_DOC):
    CASABA_DOC = CASABA_SRC_DOC
elif os.path.exists(os.path.join(sys.prefix, 'share/casaba/casaba.rst')):
    CASABA_DOC = os.path.join(sys.prefix, 'share/casaba/casaba.rst')
else:
    CASABA_DOC = '/usr/share/casaba/casaba.rst'

CASABA_VAR_DIR = '/var/tmp/casaba'
try:
    os.mkdir(CASABA_VAR_DIR, 0o700)
except OSError:
    # directory is already created, check ownership
    stat = os.stat(CASABA_VAR_DIR)
    if stat.st_uid == 0 and os.getuid() != stat.st_uid:
        print('%s is already created and owned by root. Please change '
              'ownership and try again.' % CASABA_VAR_DIR)
        sys.exit(1)
finally:
    uid, gid = get_current_user()

    if uid != 0 and os.getuid() == 0:
        try:
            os.chown(CASABA_VAR_DIR, uid, gid)
        except Exception as ex:
            print('Unable to change owner of %s. Please fix ownership '
                  'manually and try again.' % CASABA_VAR_DIR)
            sys.exit(1)

_tmpdirprefix = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-')
VAR_DIR = tempfile.mkdtemp(prefix=_tmpdirprefix, dir=CASABA_VAR_DIR)
DIR_LOG = VAR_DIR
FILE_LOG = 'casaba-setup.log'
PUPPET_MANIFEST_RELATIVE = "manifests"
PUPPET_MANIFEST_DIR = os.path.join(VAR_DIR, PUPPET_MANIFEST_RELATIVE)
HIERADATA_DIR_RELATIVE = "hieradata"
MODULE_DIR_RELATIVE = "modules"
PUPPETDATA_DIR = "/etc/puppetlabs/code/environments/"
HIERA_DIR = "/etc/puppetlabs/puppet"

API_GLOBAL_OPTIONS = UnsortableOrderedDict()

LATEST_LOG_DIR = '%s/latest' % CASABA_VAR_DIR
if os.path.exists(LATEST_LOG_DIR):
    try:
        os.unlink(LATEST_LOG_DIR)
    except OSError:
        print('Unable to delete symbol link for log dir %s.' % LATEST_LOG_DIR)

try:
    # Extract folder name at /var/tmp/casaba/<VAR_DIR> and do a relative
    # symlink to /var/tmp/casaba/latest
    os.symlink(os.path.basename(VAR_DIR),
               os.path.join(CASABA_VAR_DIR, 'latest'))
except OSError:
    print('Unable to create symbol link for log dir %s.' % LATEST_LOG_DIR)

PUPPET_DEPENDENCIES = ['puppet-agent', 'tar', 'nc']
PUPPET_SERVER_DEPENDENCIES = ['puppetserver', 'puppet-agent', 'openssh-clients', 'tar', 'nc', 'rubygems', 'rubygem-json']
PUPPET_MODULES_DEPS = ['casaba-puppet-modules']
DEVELOP_DEPS = ['git', 'gcc', 'python-devel', 'openssl-devel', 'python-pip', 'libffi-devel']

FILE_INSTALLER_LOG = "setup.log"

DIR_PROJECT_DIR = os.environ.get('INSTALLER_PROJECT_DIR', os.path.abspath(os.path.join(os.path.split(__file__)[0], '..')))
DIR_PLUGINS = os.path.join(DIR_PROJECT_DIR, "plugins")
DIR_MODULES = os.path.join(DIR_PROJECT_DIR, "modules")

EXEC_RPM = "rpm"
EXEC_SEMANAGE = "semanage"
EXEC_NSLOOKUP = "nslookup"
EXEC_CHKCONFIG = "chkconfig"
EXEC_SERVICE = "service"
EXEC_IP = "ip"

# space len size for color print
SPACE_LEN = 70
