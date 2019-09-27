# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import os

class _EnvironmentContainer(object):
    """Internal class wrapping access to environment variables."""

    @property
    def api_key(self):
        return os.environ.get("AEGISBLADE_API_KEY", None)

    @property
    def api_endpoint(self):
        return os.environ.get("AEGISBLADE_API_ENDPOINT", None)

    @property
    def default_hostdriver(self):
        return os.environ.get("AEGISBLADE_DEFAULT_HOSTDRIVER", None)

    @property
    def debug_output(self):
        return os.environ.get("AEGISBLADE_DEBUG_OUTPUT", None)
        
    @property
    def verbose_output(self):
        return os.environ.get("AEGISBLADE_VERBOSE_OUTPUT", None)

    @property
    def libraries(self):
        # type: () -> dict
        value = os.environ.get("AEGISBLADE_LIBRARIES", None)
        if value is None:
            return None

        library_dict = dict()

        for library_package_and_path in value.split(":"):
            try:
                library_package, library_path = library_package_and_path.split("=")
                library_dict[library_package] = library_path
            except Exception:
                print("Invalid AEGISBLADE_LIBRARIES format. Expected: \"package1=/some/path/1:package2=/some/path/2\"")
                raise
        
        return library_dict

    @property
    def verify_ssl(self):
        value = os.environ.get("AEGISBLADE_VERIFY_SSL", None)
        if value is None:
            return None

        if value.lower() == "true" or value == "1":
            return True
        
        return False

Environment = _EnvironmentContainer()