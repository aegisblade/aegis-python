# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

class InvalidApiKeyError(Exception):
    """An error raised when an invalid api key is provided."""

    def __init__(self, server_response_message):
        self.server_response_message = server_response_message

        self.message = "The server reported your api key is invalid. Check to ensure it's been entered correctly. " \
                       "\nServer Response: {0}".format(self.server_response_message)

    def __str__(self):
        return self.message


class ApplicationBuildError(Exception):
    """An error raised when an application fails to build."""

    def __init__(self, application_id, error_description):
        self.application_id = application_id
        self.error_description = error_description

        self.message = "An Application failed to build. File an issue at https://github.com/brthor/aegisblade if it persists. " \
                       "\n(Error Description: {0})" \
                       "\n(Application Id:{1})".format(self.error_description, self.application_id)

    def __str__(self):
        return self.message


class JobError(Exception):
    """An error raised when a job failed to begin running."""

    def __init__(self, job_id, error_description):
        self.job_id = job_id
        self.error_description = error_description

        self.message = "An Job failed to run. File an issue at https://github.com/brthor/aegisblade if it persists. " \
                       "\n(Error Description: {0})" \
                       "\n(Job Id:{1})".format(self.error_description, self.job_id)

    def __str__(self):
        return self.message


class JobRuntimeError(Exception):
    """An error raised when a job raises an Exception while running."""

    internal_error = None
    """The runtime error raised by the job while running."""

    def __init__(self, job_id, internal_error):
        # type: (str, Exception) -> None
        self.internal_error = internal_error
        self.job_id = job_id

        self.message = "A job raised an exception while running. See `internal_error` property for the exception." \
                       "\nInternal Error Type: {0}" \
                       "\nInternal Error: {1}" \
                       "\nJob Id: {2}".format(self.internal_error.__class__.__name__,
                                              str(self.internal_error),
                                              self.job_id)

    def __str__(self):
        return self.message


class UnableToDeserializeReturnValueError(Exception):
    """An error raised when a job returns a value which cannot be deserialized."""

    def __init__(self, job_id):
        self.job_id = job_id
        self.message = "A job returned a value which cannot be deserialized. " \
                       "\n(Job Id: {0})".format(self.job_id)

    def __str__(self):
        return self.message


class JobNotFoundError(Exception):
    """An error raised when a job with a specified id does not exist."""

    def __init__(self, job_id):
        self.job_id = job_id
        self.message = "A job with the specified id could not be located. " \
                       "\n(Job Id: {0})".format(self.job_id)

    def __str__(self):
        return self.message


class ApplicationNotFoundError(Exception):
    """An error raised when an application with a specified id does not exist."""

    def __init__(self, application_id):
        self.application_id = application_id
        self.message = "An application with the specified id could not be located. " \
                       "\n(Application Id: {0})".format(self.application_id)

    def __str__(self):
        return self.message
