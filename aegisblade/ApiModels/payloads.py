# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

def readFile(filePath):
    with open(filePath, 'r') as f:
        return f.read()


class HostDefinition(object):
    def __init__(self, jobConfig):
        self.driver = jobConfig.host_driver
        self.hostAffinity = jobConfig.host_affinity

        self.driverOptions = {
            'instanceType': jobConfig.host_driver_options['instanceType'],
            'region': jobConfig.host_driver_options['region'],
            'useSpotInstance': jobConfig.host_driver_options['useSpotInstance'],
            'maxSpotPrice': jobConfig.host_driver_options['maxSpotPrice']
        }


class CreateApplicationPayload(object):
    def __init__(self, applicationExecutionContext, jobConfig):
        '''
        :type applicationExecutionContext: ApplicationExecutionContext
        '''
        self.applicationExecutionContext = applicationExecutionContext
        self.hostDefinition = HostDefinition(jobConfig)
        self.capabilities = jobConfig.capabilities


class CreateJobPayload(object):
    def __init__(self, taskInfo, applicationId, jobType, clientVersion, jobConfig):
        self.jobType = jobType
        self.clientVersion = clientVersion
        self.memoryMb = jobConfig.memory
        self.applicationId = applicationId
        self.serializedJobEntrypoint = taskInfo.serializeForInjector()
        self.hostDefinition = HostDefinition(jobConfig)


class UploadFilePayload(object):
    def __init__(self, applicationContextFile=None, fileContents=None, applicationId=None):
        self.applicationContextFile = applicationContextFile
        self.applicationGuid = applicationId
        self.fileContents = fileContents

class CreateDataStorePayload(object):
    def __init__(self, dataStoreName, dataStorageDriver, dataStorageDriverOptions):
        self.dataStoreName = dataStoreName
        self.dataStorageDriver = dataStorageDriver
        self.driverOptions = dataStorageDriverOptions

