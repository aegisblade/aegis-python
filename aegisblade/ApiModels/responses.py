# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

from typing import List


class CreateApplicationResponse(object):
    """Parsed API response when creating an application."""

    error = None  # type: bool
    """`bool`: Set to True if an error occurred."""

    errorDescription = None  # type: str
    """`str`: Describes the error encountered when creating the application, if one occurred."""

    applicationId = None  # type: str
    """`str`: The GUID-like id of the application."""

    fileHashesRequiringUpload = None  # type: List[str]
    """`List[str]`: A list of hashes of files requiring upload before the application can be built."""

    def __str__(self):
        return self.__dict__.__str__()


class CreateJobResponse(object):
    """Parsed API response when creating an job."""

    error = None  # type: bool
    """`bool`: Set to True if an error occurred."""

    errorDescription = None  # type: str
    """`str`: Describes the error encountered when creating the job, if one occurred."""

    jobId = None  # type: str
    """`str`: The GUID-like id of the job."""

    jobType = None  # type: str
    """`str`: The type of job that was created."""

    def __str__(self):
        return self.__dict__.__str__()


class JobStatusResponse(object):
    """Parsed API response when fetching a job's status."""

    jobId = None  # type: str
    """`str`: The GUID-like id of the job."""

    jobStatus = None  # type: str
    """`str`: The status of the job."""

    jobType = None  # type: str
    """`str`: The type of the job."""

    errorDescription = None  # type: str
    """`str`: Describes the error encountered when running the job, if one occurred."""

    applicationId = None  # type: str
    """`str`: The GUID-like id of the application the job is a part of."""

    def __str__(self):
        return self.__dict__.__str__()


class ApplicationStatusResponse(object):
    """Parsed API response when fetching an application's status."""

    applicationId = None  # type: str
    """`str`: The GUID-like id of the application."""

    status = None  # type: str
    """`str`: The status of the job."""

    errorDescription = None  # type: str
    """`str`: Describes the error encountered when building the application, if one occurred."""

    def __str__(self):
        return self.__dict__.__str__()
