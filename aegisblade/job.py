# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import base64
import time
import sys
import pickle

from typing import Any

from aegisblade.errors import ApplicationBuildError, JobError, \
    UnableToDeserializeReturnValueError, JobRuntimeError, JobNotFoundError
from aegisblade._internal.atrace import Trace
from aegisblade.ApiModels.responses import JobStatusResponse
from aegisblade._internal.api_consumer import _AegisBladeApiConsumer
from aegisblade.application import AegisBladeApplication


class AegisBladeJob(object):
    """An object for fetching job-related information from the API.
    
    This is typically returned by a call to `aegisblade.client.AegisBladeClient.run()` but may
    be constructed from a saved `AegisBladeJob.id` by calling the 
    `AegisBladeJob.create()` method.

    In AegisBlade, a job is conceptually a task to execute part
    of an application.

    Attributes:
        id (str): The GUID-like id of the job.

        application (aegisblade.application.AegisBladeApplication): A reference to the `aegisblade.application.AegisBladeApplication` object 
            that this job is running on. See `aegisblade.application.AegisBladeApplication` docs for 
            more details.

        job_type (str): The type of job represented by this object. Currently there
            is only one job type "InstantJob".
    """


    id = None                   # type: str
    """`str`: The GUID-like id of the job."""

    application = None          # type: AegisBladeApplication
    """`aegisblade.application.AegisBladeApplication`: A reference to the `aegisblade.application.AegisBladeApplication` object that this job is running on."""

    job_type = None             # type: str
    """`str`: The type of job represented by this object."""

    _api_consumer = None         # type: AegisBladeApiConsumer
    _poll_delay = 0.7            # type: int

    @classmethod
    def create(cls, client, job_id):
        # type: (AegisBladeClient, str) -> AegisBladeJob
        """Creates an AegisBladeJob instance from a job id.

        This method will contact the API to fetch information about the job
        then return an AegisBladeJob instance.

        Args:
            client (aegisblade.client.AegisBladeClient): The AegisBlade client. The default client is imported using 'from aegisblade import aegisblade'.
            job_id (str): The id of the job corresponding to the `AegisBladeJob.id` instance property.

        Raises:
            `aegisblade.errors.JobNotFoundError`: A job with the specified id was not found.
        """
        api_consumer = client._get_api_consumer()    # type: AegisBladeApiConsumer
        
        try:
            job_info = api_consumer.job_status(job_id)
        except Exception as e:
            if 'job not found' in str(e).lower():
                raise JobNotFoundError(job_id)

            raise

        return cls(client._get_api_consumer(), job_id, job_info.applicationId, job_info.jobType)

    def __init__(self, api_consumer, job_id, application_id, job_type):
        # type: (AegisBladeApiConsumer, str, str, str) -> None
        """The constructor is not recommended for direct use. 
        Use `AegisBladeJob.create()` to get an `AegisBladeJob` instance.
        """
        self._api_consumer = api_consumer
        self.id = job_id

        self.application = AegisBladeApplication(api_consumer, application_id)
        self.job_type = job_type

    def get_status(self):
        # type: () -> JobStatusResponse
        """
        Retrieves the status of this job from AegisBlade servers.

        Returns:
            `aegisblade.ApiModels.responses.JobStatusResponse`:  An object detailing the status of the job and any errors encountered
        """
        job_status_response = self._api_consumer.job_status(self.id)
        return job_status_response

    def get_logs(self):
        # type: () -> str
        """
        Retrieves the stdout & stderr logs output by the job while running.
        
        Returns:
            `str`: The stdout & stderr logs output by the job while running.
        """
        logs = self._api_consumer.job_logs(self.id)
        return logs

    def is_completed(self):
        # type: () -> bool
        """
        Returns whether or not the job has completed running. 
        
        Returns:
            `bool`: Whether or not the job has completed running.
        """
        status = self.get_status()

        return self._is_completed(status)

    def get_return_value(self, timeout=None):
        # type: (float) -> Any
        """Waits for the job to complete, and then fetches the serialized return value, deserializes it and returns it.

        Args:
            timeout (float): Timeout in seconds for waiting for job to complete, defaults to no timeout.

        Returns:
            `Any`: The deserialized value returned by the job's target Callable.

        Raises:
            `aegisblade.errors.JobRuntimeError`: The job raised an exception while running. The runtime exception is captured in `aegisblade.errors.JobRuntimeError.internal_error`.

            `aegisblade.errors.UnableToDeserializeReturnValueError`: The return value was unable to be deserialized.

        """
        self.wait_until_completed(timeout=timeout)

        serialized_return_value_str = self._api_consumer.job_return_value(self.id)

        try:
            return_value = pickle.loads(
                base64.b64decode(serialized_return_value_str))
        except:
            raise UnableToDeserializeReturnValueError(self.id)

        if issubclass(return_value.__class__, BaseException):
            Trace.debug("[DEBUG] Exception as return value.")
            Trace.debug(return_value)
            raise JobRuntimeError(self.id, return_value)

        return return_value

    def wait_until_completed(self, timeout=None):
        # type: (float) -> JobStatusResponse
        """Waits for the job to complete.

        Args:
            timeout (float): Timeout in seconds for waiting for job to complete, defaults to no timeout.
        """
        start_time = time.time()

        Trace.verbose("[INFO] Waiting until job completion ({0})".format(self.id))

        while True:
            status = self.get_status()

            if self._is_completed(status):
                Trace.verbose("[INFO] Job completed. ({0})".format(self.id))
                Trace.debug("[DEBUG] Job completed ({0}), status output: {1}".format(self.id, status))

                self._raise_job_error_if_applicable(status)

                return status

            time.sleep(self._poll_delay)

            if timeout is not None and (time.time() - start_time) > timeout:
                raise Exception("Timed out while waiting for job to complete")

    def _is_completed(self, status):
        # type: (JobStatusResponse) -> bool
        completed_states = ["finished", "canceled", "error"]

        return status.jobStatus.lower() in completed_states

    def _has_error(self, status):
        # type: (JobStatusResponse) -> bool
        error_states = ["error"]
        return status.jobStatus.lower() in error_states

    def _has_application_error(self, status):
        # type: (JobStatusResponse) -> bool
        if not self._has_error(status):
            return False

        return 'application failed to build' in status.errorDescription.lower()

    def _raise_job_error_if_applicable(self, status):
        if self._has_application_error(status) and self.application is not None:
            application_status = self.application.get_status()

            Trace.debug("[DEBUG] Error building application.")
            Trace.debug("[DEBUG] Application Status: {0}".format(application_status))

            raise ApplicationBuildError(self.application.id, application_status.errorDescription)

        if self._has_error(status):
            Trace.debug("[DEBUG] Error running job.")
            Trace.debug("[DEBUG] " + status.errorDescription)

            raise JobError(self.id, status.errorDescription)
