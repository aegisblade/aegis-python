# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import requests, shutil, functools, os, tempfile
from requests import HTTPError
from requests.utils import super_len

from aegisblade.ApiModels.payloads import CreateJobPayload, UploadFilePayload, CreateApplicationPayload, CreateDataStorePayload
from aegisblade.ApiModels.responses import JobStatusResponse, CreateJobResponse, CreateApplicationResponse, \
    ApplicationStatusResponse
from aegisblade._internal.application_context_file import ApplicationContextFile
from aegisblade._internal.application_execution_context import ApplicationExecutionContext
from aegisblade.errors import InvalidApiKeyError
from aegisblade.job_config import JobConfig
from aegisblade._internal.task_info import TaskInfo
from aegisblade._internal.json_wrapper import json_encode, json_decode
from aegisblade.__version__ import __version__


class _AegisBladeApiConsumer(object):
    """Internal class that abstracts the HTTP interface of the AegisBlade API.
    """
    def __init__(self, api_key, service_url="https://localhost:5000/api/v1", verify_ssl=True):
        self.service_url = service_url
        self.api_key = api_key
        self.verify_ssl = verify_ssl

    def create_application(self, application_execution_context, job_config):
        # type: (ApplicationExecutionContext, JobConfig) -> CreateApplicationResponse
        url = self.service_url + "/application/create"

        post_data = CreateApplicationPayload(application_execution_context, job_config)
        post_data = json_encode(post_data)

        response = requests.post(url, data=post_data, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        application_response = json_decode(response.text, CreateApplicationResponse)

        return application_response

    def application_status(self, application_guid):
        # type: (str) -> ApplicationStatusResponse
        '''
        :type application_guid: str
        :rtype: ApplicationStatusResponse
        '''
        url = self.service_url + "/application/status/" + application_guid

        response = requests.get(url, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        job_response = json_decode(response.text, ApplicationStatusResponse)
        return job_response

    def upload_file(self, application_id, application_context_file):
        # type: (str, ApplicationContextFile) -> str
        url = self.service_url + "/application/upload"

        post_data = UploadFilePayload(application_context_file, application_context_file._x_fileContents, application_id)
        post_data = json_encode(post_data)

        response = requests.post(url, data=post_data, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        return response.text

    def create_instant_job(self, task_info, application_id, job_config):
        # type: (TaskInfo, str, JobConfig) -> CreateJobResponse
        url = self.service_url + "/job/create"

        post_data = CreateJobPayload(task_info, application_id, "instant",
                                    __version__, job_config)
        post_data = json_encode(post_data)

        response = requests.post(url, data=post_data, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        job_response = json_decode(response.text, CreateJobResponse)

        return job_response

    def job_status(self, job_guid):
        # type: (str) -> JobStatusResponse
        url = self.service_url + "/job/status/" + job_guid

        response = requests.get(url, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        job_response = json_decode(response.text, JobStatusResponse)
        return job_response

    def _get_default_headers(self, content_type="application/json"):
        return {
            "Content-Type": content_type,
            "Authorization": "bearer " + self.api_key
        }

    def job_logs(self, job_guid):
        # type: (str) -> str
        url = self.service_url + "/job/logs/" + job_guid

        response = requests.get(url, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        return response.text

    def job_return_value(self, job_guid):
        # type: (str) -> str
        url = self.service_url + "/job/returnvalue/" + job_guid

        response = requests.get(url, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        return response.text

    def data_store_create(self, data_store_name, data_storage_driver, driver_options):
        url = self.service_url + "/data/store/create"

        post_data = CreateDataStorePayload(data_store_name, data_storage_driver, driver_options)
        post_data = json_encode(post_data)

        response = requests.post(url, data=post_data, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        return response.text

    def data_store_delete(self, data_store_name):
        url = self.service_url + "/data/store/{0}/delete".format(data_store_name)

        response = requests.delete(url, headers=self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        return response.text

    def data_store_upload(self, data_store_name, data_store_path, data):
        url = self.service_url + "/data/store/{0}/file/{1}".format(data_store_name, data_store_path)

        response = requests.put(url, data=data, 
            headers=self._get_default_headers(content_type="application/octet-stream"), 
            verify=self.verify_ssl,
            allow_redirects=False)
        self._handle_potential_error(response)
        
        # Redirects are expected
        if response.status_code != 302:
            return
        
        redirect_url = response.headers.get('location')

        if hasattr(data, 'seek'):
            data.seek(0)

        response2 = requests.put(redirect_url, data=data, 
            headers={'Content-Type': "application/octet-stream"}, 
            verify=True,
            allow_redirects=True,
            stream=True)
        
        self._handle_potential_error(response2)


    def data_store_delete_file(self, data_store_name, data_store_path):
        url = self.service_url + "/data/store/{0}/file/{1}".format(data_store_name, data_store_path)

        response = requests.delete(url, 
            headers=self._get_default_headers(), 
            verify=self.verify_ssl)

        self._handle_potential_error(response)

        return response.text

    def data_store_download(self, data_store_name, data_store_path):
        url = self.service_url + "/data/store/{0}/file/{1}".format(data_store_name, data_store_path)

        temp_file = os.path.join(tempfile.mkdtemp(), os.path.basename(data_store_path))

        redirect_url = self._stream_download_file(url, 
            temp_file, self._get_default_headers(), self.verify_ssl, False)

        # Storage driver specific url redirections are expected
        if redirect_url:
            self._stream_download_file(redirect_url, temp_file, None, True, True)

        return temp_file

    def data_store_list_files(self, data_store_name):
        url = self.service_url + "/data/store/{0}/list".format(data_store_name)

        response = requests.get(url, headers = self._get_default_headers(), verify=self.verify_ssl)
        self._handle_potential_error(response)

        json_response = response.json()

        return json_response

    def _stream_download_file(self, url, local_filename, headers, verify_ssl, allow_redirects):
        with requests.get(url, stream=True, headers=headers, verify=verify_ssl, allow_redirects=allow_redirects) as r:
            if (r.status_code == 302):
                return r.headers.get('location')

            r.raise_for_status()

            r.raw.read = functools.partial(r.raw.read, decode_content=True)

            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return None

    def _handle_potential_error(self, response):
        # type: (requests.Response) -> None

        # Authentication Error
        if response.status_code == 401 and response.headers.get('www-authenticate', None) is not None:
            raise InvalidApiKeyError(
                "The server reported your api key is invalid. Check to ensure it's been entered correctly. "
                "Server Response: {0}".format(response.headers.get('www-authenticate')))

        # Any kind of error where the server returns a json message
        if response.status_code not in [200, 201] \
                and response.headers.get("content-type", "").startswith("application/json"):
            try:
                response_json = response.json()
                error_message = response_json.get("errorMessage", None)
            except ValueError as e:
                if 'json' not in str(e).lower():
                    raise

                error_message = None

            if error_message is not None:
                raise HTTPError(error_message, response=response)

        # Catch-All
        response.raise_for_status()

