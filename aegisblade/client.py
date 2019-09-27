# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import base64
import inspect

import time
from aegisblade._internal.atrace import Trace

import os
import sys

import pickle
from typing import Callable, List

from aegisblade._internal.api_consumer import _AegisBladeApiConsumer
from aegisblade._internal.application_execution_context_collector import _ApplicationExecutionContextCollector
from aegisblade._internal.task_info import TaskInfo
from aegisblade.job import AegisBladeJob
from aegisblade.job_config import JobConfig
from aegisblade.data_store import DataStore

from aegisblade._internal.environment import Environment

class AegisBladeClient(object):
    """AegisBlade client. Provides easy methods for starting jobs,
    and accessing data files.

    The client may be configured by using its methods such as `AegisBladeClient.set_api_key()`
    or by the use of the following environment variables:

    Environment:

        AEGISBLADE_API_KEY: Your api key.

        AEGISBLADE_DEFAULT_HOSTDRIVER: The default hostdriver to use such as 'ec2'.

        AEGISBLADE_VERIFY_SSL: Whether or not to verify the ssl certs of the endpoint. Testing purposes only.

        AEGISBLADE_API_ENDPOINT: The service endpoint. Testing purposes only.

        AEGISBLADE_DEBUG_OUTPUT: Enable debug console output.

    """
    _api_key = None
    _service_url = None

    _verify_ssl = True

    _default_endpoint = "https://www.aegisblade.com"
    _default_service_path = "/api/v1"

    def __init__(self, verify_ssl=True):
        """Initializes the AegisBlade client and uses the environment
        variables described in the class documentation to set values.
        """
        self.set_api_key(Environment.api_key)
        self.set_api_endpoint(Environment.api_endpoint or self._default_endpoint)
        
        env_verify_ssl = Environment.verify_ssl
        if env_verify_ssl is not None:
            self.set_verify_ssl(env_verify_ssl)

    def set_verify_ssl(self, verify_ssl):
        # type: (bool) -> None
        """Sets whether or not to verify the ssl certificates of the API endpoint.
        Not recommended outside of internal use.
        """
        if not isinstance(verify_ssl, bool):
            raise TypeError("Invalid verify_ssl type, expected bool.")

        self._verify_ssl = verify_ssl

    def set_api_key(self, api_key):
        """Sets the api key used by this client to access the AegisBlade API."""
        self._api_key = api_key

    def set_api_endpoint(self, endpoint):
        """Sets the api endpoint used by this client. 
        Not recommended outside of internal use.
        """
        if not endpoint:
            raise ValueError("Invalid endpoint value.")

        self.api_endpoint = endpoint

        self.set_service_url(self.api_endpoint + self._default_service_path)

    def set_service_url(self, service_url):
        """Sets the full service url (e.g. endpoint + path) used by this client. 
        Not recommended outside of internal use.
        """
        self._service_url = service_url

    def data(self, data_store_name):
        # type: (string) -> DataStore
        """Used to access the data store api. The data store can be used to 
        store arbitrary data accessible by any job or machine with internet 
        access (and the proper api key).

        Args:
            data_store_name (str): The name of the data store you want to access. 
                If it is not already created, you will need to call `aegisblade.data_store.DataStore.create()` 
                on the return value of this function.

        Returns:
            `aegisblade.data_store.DataStore`: A `aegisblade.data_store.DataStore` object which acts as a container of data files that you 
            may upload, download, or delete using the object. See `aegisblade.data_store.DataStore` class
            docs for more detail. 

        """
        return DataStore(data_store_name, self._get_api_consumer())

    def run(self, remotely_executed_callable, job_config=None):
        # type: (Callable, JobConfig) -> AegisBladeJob
        """Creates and runs a job on AegisBlade.
        
        When called this function will first create an application by uploading
        .py files found inside the current working directory tree, determine 
        libraries by calling 'pip freeze', and upload local libraries explicitly
        defined by the job_config argument.

        Refer to the `AegisBladeClient.get_upload_files()` method if you wish to 
        preview the files that will be uploaded, prior to running a job.

        After the files are uploaded successfully, AegisBlade will build an 
        application image that can be deployed and run on any number of machines.
        Jobs created as a part of this application will need to wait for it to finish
        building before running. The length of the build depends primarily upon the
        time required to install the various dependencies of the application.

        Applications are cached by AegisBlade, and subsequent calls to this function
        will only upload updated files. If no files have been updated, the same 
        application will be used, and created jobs will not need to wait for it to build.

        This function will queue a job to be run as a part of the application immediately
        after creating it and uploading the files. 
        
        Any number of jobs may be queued for an application, and there is no need to wait 
        for an application to be finished building or for the first job to run before 
        queuing more jobs.

        The returned object of this function may be used to check on the status of the job
        or application, or you can use the web ui available at https://www.aegisblade.com/app.

        Args:
            remotely_executed_callable (Callable): The target function you wish to execute.

            job_config (aegisblade.job_config.JobConfig): An optional JobConfig object used to configure
                various properties of the job such as required memory, and local libraries. 
                See JobConfig class documentation for more details.

        Returns:
            An `aegisblade.job.AegisBladeJob` class instance. This class may be used to fetch the job status,
            synchronously wait for it to finish, fetch logs, and fetch the return value.

            The `aegisblade.job.AegisBladeJob.id` property of the AegisBladeJob instance may be saved and used to get 
            information on the job at a later time.
        """
        if not callable(remotely_executed_callable):
            raise Exception("Must pass callable as first argument to AegisBlade.")

        if not self._api_key:
            raise Exception("The api key was not specified. Call `.set_api_key()` or set the AEGISBLADE_API_KEY environment variable.")


        job_config = job_config or JobConfig()

        task_info = TaskInfo(remotely_executed_callable)
        application_execution_context = _ApplicationExecutionContextCollector().collect(job_config.libraries)

        api_consumer = self._get_api_consumer()

        create_application_response = self._create_application(api_consumer, application_execution_context, job_config)

        self._upload_application_files(api_consumer, application_execution_context, create_application_response)
        create_job_response = self._create_job(api_consumer, task_info, create_application_response, job_config)

        return AegisBladeJob(api_consumer, create_job_response.jobId, create_application_response.applicationId, create_job_response.jobType)

    def get_upload_files(self, job_config):
        # type: (JobConfig) -> List[str]
        """Returns a list of files that will be uploaded as part of the
        application build. It DOES NOT upload any files or contact the API.

        This method exists so developers can check what files are going
        to be uploaded when they call `AegisBladeClient.run()`. 
        """
        job_config = job_config or JobConfig()

        application_execution_context = _ApplicationExecutionContextCollector().collect(job_config.libraries)

        local_upload_paths = []

        for application_file in application_execution_context.files:
            local_upload_paths.append(application_file.filePath)

        return local_upload_paths

    def _get_api_consumer(self):
        # type: () -> AegisBladeApiConsumer
        return _AegisBladeApiConsumer(self._api_key, service_url=self._service_url, verify_ssl=self._verify_ssl)

    def _create_application(self, api_consumer, application_execution_context, job_config):
        # type: (AegisBladeApiConsumer, ApplicationExecutionContext, JobConfig) -> CreateApplicationResponse
        create_application_response = api_consumer.create_application(application_execution_context, job_config)

        if create_application_response.error:
            raise Exception("Failed to create application. Error: {0}".format(create_application_response.errorDescription))

        Trace.verbose("[INFO] Application Created ({0}).".format(create_application_response.applicationId))

        return create_application_response

    def _upload_application_files(self, api_consumer, application_execution_context, create_application_response):
        # type: (AegisBladeApiConsumer, ApplicationExecutionContext, CreateApplicationResponse) -> None
        for count, upload_file_hash in enumerate(create_application_response.fileHashesRequiringUpload):
            app_file = [x for x in application_execution_context.files if x.fileHash == upload_file_hash][0]

            Trace.verbose("[INFO] Uploading File {0}/{1} ({2})"
                          .format(count+1,
                                  len(create_application_response.fileHashesRequiringUpload),
                                  app_file.filePathRelativeToAppContext))

            api_consumer.upload_file(create_application_response.applicationId, app_file)

    def _create_job(self, api_consumer, task_info, create_application_response, job_config):
        # type: (AegisBladeApiConsumer, TaskInfo, CreateApplicationResponse, JobConfig) -> CreateJobResponse
        Trace.verbose("[INFO] Creating Job.")
        create_job_response = api_consumer.create_instant_job(task_info, create_application_response.applicationId, job_config)

        if create_job_response.error:
            raise Exception("Failed to create job. Error: {0}".format(create_job_response.errorDescription))

        Trace.verbose("[INFO] Job Created ({0})".format(create_job_response.jobId))
        return create_job_response
