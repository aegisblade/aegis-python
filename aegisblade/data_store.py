# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import shutil


class DataStore(object):
    """A utility for accessing data stores and their files.

    A Data Store is a logical "drive" of files that is backed
    by your choice of driver (AWS S3 only currently). Before
    uploading files or other operations the data store must be
    created with a call to `DataStore.create()`.

    Each data store is identified by a unique name, and can 
    be accessed from any job or machine with access to the proper
    API Key. 

    The data store is typically used to save results from jobs or 
    put up data that can be accessed by any of your jobs.

    Attributes:
        name (str): The name of the data store.

    """

    name = None
    """`str`: The name of the data store."""


    def __init__(self, name, api_consumer):
        # type: (str, AegisBladeApiConsumer) -> None
        """The constructor is not recommended for direct use. 
        Use `aegisblade.client.AegisBladeClient.data()` to get a `DataStore` instance.

        Call `DataStore.create()` to create the data store if it does
        not already exist.
        """

        self.name = name
        """`str`: The name of the data store."""

        self.api_consumer = api_consumer

    def create(self, driver, driver_options):
        # type: (string, dict) -> DataStore
        """Creates the data store using the specified backing driver
        and options for that driver.

        Args:
            driver (str): The driver to use for backing the data store ("s3" only currently.)

            driver_options (dict): A dictionary of options specific to the driver. 
                (e.g. "region" may be defined for s3)
        """
        self.api_consumer.data_store_create(self.name, driver, driver_options)

        return self

    def upload_file(self, local_file_path, data_store_path):
        # type: (str, str) -> None
        """Uploads a file from the local machine to the data store.
        
        Args:
            local_file_path (str): The path of the file to upload on the local machine.

            data_store_path (str): The storage path of the file inside the data store.
        """
        with open(local_file_path, 'rb') as f:
            self.api_consumer.data_store_upload(self.name, data_store_path, f)

    def upload_data(self, data, data_store_path):
        # type: (str, str) -> None
        """Uploads a string to the data store.
        
        Args:
            data (str): The data string to store in the data store.

            data_store_path (str): The path in which to store the data inside the data store.
        """
        self.api_consumer.data_store_upload(self.name, data_store_path, data)

    def download(self, data_store_path):
        # type: (str) -> str
        """Downloads data from the data store and returns it as a string.

        Args:
            data_store_path (str): The path of the data inside the data store to download.

        Returns:
            `str`: The downloaded data as a string.

            On Python3 this will return a `bytes` object.
        """
        tmp_file = self.api_consumer.data_store_download(self.name, data_store_path)
        
        with open(tmp_file, 'rb') as f:
            return f.read()

    def download_to_file(self, data_store_path, local_file):
        # type: (str, str) -> None
        """Downloads data from the data store and writes it to a local file.

        Args:
            data_store_path (str): The path of the data inside the data store to download.
            
            local_file (str): Path of a local file that the data will be written to.
        """
        tmp_file = self.api_consumer.data_store_download(self.name, data_store_path)

        shutil.copyfile(tmp_file, local_file)

    def delete(self, data_store_path):
        # type: (str) -> None
        """Deletes the specified data from the data store.

        Args:
            data_store_path (str): Path of the data inside the data store to delete.
        """
        self.api_consumer.data_store_delete_file(self.name, data_store_path)

    def delete_store(self):
        """Deletes this entire data store and all files in it.

        USE CAREFULLY!
        """
        self.api_consumer.data_store_delete(self.name)

    def list_files(self):
        """Lists all files in the data store.

        Returns:
            `List str`: A list of all files in the data store.
        """
        return self.api_consumer.data_store_list_files(self.name)
