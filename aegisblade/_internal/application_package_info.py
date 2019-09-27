# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

class ApplicationPackageInfo(object):
    """Stores information related to a 'pip install'ed package
    in the current environment.

    Attributes:
        name (str): Name of the package

        version (str): Full version of the package.
    """

    name = None     # type: str
    version = None  # type: str

    def __init__(self, name, version):
        """Initializes the ApplicationPackageInfo.

        Args:
            name (str): Name of the package

            version (str): Full version of the package.
        """
        self.name = name
        self.version = version