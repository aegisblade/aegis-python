# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

from typing import List

from aegisblade._internal.application_package_info import ApplicationPackageInfo
from aegisblade._internal.application_context_file import ApplicationContextFile


class ApplicationExecutionContext(object):
    """Encapsulates the data required to build an executable 
    version of the application on AegisBlade.

    Attributes:
        language (str): The programming language used in the application. "python" in this case.

        sourceRuntimeIdentifier (str): OS Identier of the source machine. Used for diagnostic purposes.

        packages (List aegisblade.application_package_info.ApplicationPackageInfo): List of Application dependency packages, Name, Version pairs.

        files (List aegisblade.application_context_file.ApplicationContextFile): List of Application files which are required for the program to function as expected.

        targetRuntimeName (str): Not used in python.

        targetRuntimeVersion (str): Python version.

        packageManagerSourceFeeds (List str): Source feeds for packages used by your application. Not currently used in python.

        clientVersion (List): Version of this client.
    """

    packageManagerSourceFeeds = None    # type: List[str]
    targetRuntimeVersion = None         # type: str
    targetRuntimeName = None            # type: str
    files = None                        # type: List[ApplicationContextFile]
    packages = None                     # type: List[ApplicationPackageInfo]
    language = None                     # type: str
    sourceRuntimeIdentifier = None      # type: str
    clientVersion = None                # type: str

    def __init__(self,
                 language,
                 source_runtime_identifier,
                 packages,
                 files,
                 target_runtime_name,
                 target_runtime_version,
                 package_manager_source_feeds,
                 client_version):
        # type: (str, str, List[ApplicationPackageInfo], List[ApplicationContextFile], str, str, List[str], str) -> None
        """Initializes the ApplicationExecutionContext.

        Args:
            language (str): The programming language used in the application. "python" in this case.

            sourceRuntimeIdentifier (str): OS Identier of the source machine. Used for diagnostic purposes.

            packages (List aegisblade.application_package_info.ApplicationPackageInfo): List of Application dependency packages, Name, Version pairs.

            files (List aegisblade.application_context_file.ApplicationContextFile): List of Application files which are required for the program to function as expected.

            targetRuntimeName (str): Not used in python.

            targetRuntimeVersion (str): Python version.

            packageManagerSourceFeeds (List str): Source feeds for packages used by your application. Not currently used in python.

            clientVersion (List): Version of this client.
        """
        self.packageManagerSourceFeeds = package_manager_source_feeds
        self.targetRuntimeVersion = target_runtime_version
        self.targetRuntimeName = target_runtime_name
        self.files = files
        self.packages = packages
        self.language = language
        self.sourceRuntimeIdentifier = source_runtime_identifier
        self.clientVersion = client_version

