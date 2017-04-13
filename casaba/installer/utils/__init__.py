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

from .datastructures import SortedDict
from .decorators import retry
from .network import get_localhost_ip
from .network import host2ip
from .network import force_ip
from .network import device_from_ip
from .shell import execute
from .shell import ScriptRunner
from .shortcuts import host_iter
from .shortcuts import hosts
from .shortcuts import get_current_user
from .shortcuts import get_current_username
from .shortcuts import split_hosts
from .strings import COLORS
from .strings import color_text
from .strings import mask_string
from .strings import state_format
from .strings import state_message


__all__ = ('SortedDict',
           'retry',
           'get_localhost_ip', 'host2ip', 'force_ip', 'device_from_ip',
           'ScriptRunner', 'execute',
           'host_iter', 'hosts', 'get_current_user', 'get_current_username',
           'split_hosts', 'COLORS', 'color_text', 'mask_string',
           'state_format', 'state_message')
