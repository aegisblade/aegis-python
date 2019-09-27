# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import base64
import sys


class ApplicationContextFile(object):
    """Represents a file required for execution of the current application.

    This class encapsulates all details required to determine if the file has
    changed from previous iterations, and to upload the file if needed.

    Attributes:
        fileHash (str): The sha256 hash of the file's contents.

        filePathRelativeToAppContext (str): The relative path of the file to CWD.

        filePath (str): Absolute path of the file on the source machine.

        fileByteCount (int): The number of bytes in the file.

        _x_fileContents (str): Base64 encoded string of the file's contents. 
            The strange '_x_' naming is a convention used to prevent 
            automatically serializing this value to json.
    """
    
    fileHash = None                      # type: str
    """`str`: The sha256 hash of the file's contents."""

    filePathRelativeToAppContext = None  # type: str
    """`str`: The relative path of the file to CWD."""

    filePath = None                      # type: str
    """`str`: Absolute path of the file on the source machine."""

    fileByteCount = None                 # type: int
    """`int`: The number of bytes in the file."""

    _x_fileContents = None               # type: str
    """`str`: Base64 encoded string of the file's contents."""

    def __init__(self, file_path, file_path_relative_to_app_context, file_hash, file_contents, file_byte_count):
        self.fileHash = file_hash
        self.filePathRelativeToAppContext = file_path_relative_to_app_context
        self.filePath = file_path
        self.fileByteCount = file_byte_count

        self._x_fileContents = base64.b64encode(file_contents)
        
        if sys.version_info[0] == 3:
            self._x_fileContents = self._x_fileContents.decode('ascii')