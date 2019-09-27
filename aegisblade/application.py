# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

from aegisblade.ApiModels.responses import ApplicationStatusResponse
from aegisblade._internal.api_consumer import _AegisBladeApiConsumer


class AegisBladeApplication(object):
    """An object for fetching and storing application-related information 
    from the API.

    This is typically returned by a call to `aegisblade.client.AegisBladeClient.run()` but may
    be constructed from a saved `AegisBladeApplication.id` by calling the 
    `AegisBladeApplication.create()` method.

    In AegisBlade, an application is the collection of files, packages, 
    libraries, and capabilities that constitute an executable codebase.
    
    These constituents are collected and constructed into a deployable image
    during the application build. Then any number of jobs can be defined to
    run on top of this application image.

    Attributes:
        id (str): The GUID-like id of the application.
    """

    id = None               # type: str
    """`str`: The GUID-like id of the application."""

    _api_consumer = None     # type: AegisBladeApiConsumer

    @classmethod
    def create(cls, client, application_id):
        # type: (AegisBladeClient, str)
        """Creates an AegisBladeApplication instance from an application id.

        Args:
            client (aegisblade.client.AegisBladeClient): The AegisBlade client. The default client is imported 
                using 'from aegisblade import aegisblade'.

            application_id (str): The id of the application corresponding to the 
                `AegisBladeApplication.id` instance property.
        """
        return cls(client._get_api_consumer(), application_id)

    def __init__(self, api_consumer, application_id):
        # type: (AegisBladeApiConsumer, str) -> None
        self._api_consumer = api_consumer
        self.id = application_id

    def get_status(self):
        # type: () -> ApplicationStatusResponse
        """Gets the status information of the application from the API.

        Returns:
            aegisblade.ApiModels.responses.ApplicationStatusResponse
        """
        return self._api_consumer.application_status(self.id)
