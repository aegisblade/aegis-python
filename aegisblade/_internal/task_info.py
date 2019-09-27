# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import base64
import sys
import cloudpickle
from typing import Callable


class TaskInfo(object):
    """Wraps and serializes the callable to be run as part of a job.

    Attributes:
        func: The callable to be run as part of a job.
    """

    func = None  # type: Callable

    def __init__(self, func):
        # type: (Callable) -> None
        self.func = func

    def serializeForInjector(self):
        # type: () -> str
        ret = cloudpickle.dumps(self.func)
        ret = base64.b64encode(ret)
        
        if sys.version_info[0] == 3:
            ret = ret.decode('ascii')
            
        return ret
