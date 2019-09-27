# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import os

from aegisblade._internal.environment import Environment


class Trace(object):
    """Internal class for outputting debug information to the console."""
    @classmethod
    def debug_output_level(cls):
        return Environment.debug_output is not None

    @classmethod
    def verbose_output_level(cls):
        return cls.debug_output_level() or Environment.verbose_output is not None

    @classmethod
    def debug(cls, message):
        if cls.debug_output_level():
            print(message)

    @classmethod
    def verbose(cls, message):
        if cls.verbose_output_level():
            print(message)
