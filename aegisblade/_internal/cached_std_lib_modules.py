# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import sys
import os
import imp


def get_std_lib_modules():
    current_version_str = '{0}.{1}'.format(*sys.version_info)
    return get_python_version_std_lib_modules(current_version_str)


def get_python_version_std_lib_modules(python_version):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(file_dir, '_cached_stdlib_modules','v{0}.py'.format(python_version.replace('.', '_')))

    if not os.path.isfile(target_file):
        raise Exception(
            "Python version {0} not yet supported. "
            "See https://github.com/brthor/aegisblade for more info.".format(python_version))

    file_module = imp.load_source('stdlib', target_file)
    return file_module.__content__

    # std_lib_modules = []
    # with open(target_file, 'r') as f:
    #     for line in f:
    #         module_name = line.replace("\n", "").replace("\r", "")
    #         std_lib_modules.append(module_name)

    # return std_lib_modules
