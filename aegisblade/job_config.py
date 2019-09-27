# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

from typing import Optional, Dict, Any
import os

from aegisblade._internal.environment import Environment

try:
  basestring
except NameError:
  basestring = str

class JobConfig(object):
    """Configuration container for a job.

    The JobConfig is an optional object that can be used to
    specify configuration that will change the way a job is 
    executed, determine host placement, or configure values
    for the backing host driver.

    Attributes:
        libraries (Dict str=str): A dictionary of `package=local_path` of local
            packages used inside the project from outside the 
            project's directory tree. These libraries will be 
            uploaded as part of your application and put on the
            `PYTHONPATH` during its execution.

        memory (int): The amount of memory in MB required by the job. Used
            to determine how many jobs will be run per host. Specifying
            an amount greater than the instance type specified in 
            `JobConfig.host_driver_options` (or the default instance type), will not
            change the instance type to accomodate the greater amount
            of memory, but will force only one job to run per host.

        host_driver (str): The backing driver to use in launching the hosts
            for the job. ("ec2" only currently).
        
        host_driver_options (Dict str=Any): A dict of options for the host driver such
            as "instanceType", "region", and "useSpotInstance".

        host_affinity (str): A string label used to group jobs on a host(s). If 
            specified, the job will only run on hosts with the same host
            affinity label. For example, assigning "host1" to jobs 1-4 and
            "host2" to jobs 5-8 will force both sets of jobs to run on 
            different hosts regardless of other factors.
        
        capabilities (List `aegisblade.capabilities.Capability`): An array of capabilities required by this job. See
            `aegisblade.capabilities.Capability` for more details.
    """

    _default_memory = 1024
    _default_host_driver = "ec2"
    _default_host_driver_options = {
        'instanceType': None,
        'region': None, 
        'useSpotInstance': True,
        'maxSpotPrice': None
    }

    libraries = None  # type: Dict[str, str]
    """`Dict str=str`: A dictionary of `package=local_path` of local
            packages used inside the project from outside the 
            project's directory tree. These libraries will be 
            uploaded as part of your application and put on the
            `PYTHONPATH` during its execution."""

    memory = None     # type: int
    """`int`: The amount of memory in MB required by the job. Used
            to determine how many jobs will be run per host. Specifying
            an amount greater than the instance type specified in 
            `JobConfig.host_driver_options` (or the default instance type), will not
            change the instance type to accomodate the greater amount
            of memory, but will force only one job to run per host."""

    host_driver = None  # type: str
    """`str`: The backing driver to use in launching the hosts
            for the job. ("ec2" only currently)."""

    host_driver_options = None  # type: Dict[str, Any]
    """`Dict str=Any`: A dict of options for the host driver such
            as "instanceType", "region", and "useSpotInstance"."""

    host_affinity = None  # type: str
    """`str`: A string label used to group jobs on a host(s). If 
            specified, the job will only run on hosts with the same host
            affinity label. For example, assigning "host1" to jobs 1-4 and
            "host2" to jobs 5-8 will force both sets of jobs to run on 
            different hosts regardless of other factors."""

    capabilities = None  # type: List[aegisblade.capabilities.Capability]
    """`List` `aegisblade.capabilities.Capability`: An array of capabilities required by this job. See
            `aegisblade.capabilities.Capability` for more details."""

    def __init__(self):
        # type: (int, string, string, dict, list) -> None
        """Constructor intializes a `JobConfig` with default options."""
        self.libraries = {}
        self.memory = self._default_memory
        self.host_driver = Environment.default_hostdriver or self._default_host_driver
        self.host_driver_options = self._default_host_driver_options
        self.host_affinity = None
        self.capabilities = []

        env_libraries = Environment.libraries or dict()
        self.with_libraries(env_libraries)
    
    def with_memory(self, memory):
        # type: (int) -> JobConfig
        """Sets the amount of memory in MB required by the job.

        See the `JobConfig.memory` docs for more details on how memory is used.

        Args:
            memory (int): Amount of memory in MB.
        """
        if type(memory) is not int:
            raise TypeError('memory must be an int')

        self.memory = memory

        return self

    def with_host_driver(self, host_driver, host_driver_options=None):
        # type: (str, Optional[dict]) -> JobConfig
        """Sets the host driver and options for that driver to be used
        when starting the job.

        See the `JobConfig.host_driver` and `JobConfig.host_driver_options` docs for more detail.

        Args:
            host_driver (str): See `JobConfig.host_driver`

            host_driver_options (Dict str=Any): See `JobConfig.host_driver_options`

        """
        if type(host_driver) is not str:
            raise TypeError('host_driver must be a str')

        if host_driver_options is not None and type(host_driver_options) is not dict:
            raise TypeError('host_driver_options must be a dict')

        self.host_driver = host_driver

        if host_driver_options:
            self.host_driver_options = self._merge_default_dict(self._default_host_driver_options, host_driver_options)
        elif not self.host_driver_options:
            self.host_driver_options = self._default_host_driver_options

        return self

    def with_host_affinity(self, host_affinity):
        # type: (str) -> JobConfig
        """Sets the host affinity for the job.

        See the `JobConfig.host_affinity` doc for more details.

        Args:
            host_affinity (str): See `JobConfig.host_affinity`
        """
        if host_affinity is not None and type(host_affinity) is not str:
            raise TypeError('host_affinity must be a str')

        self.host_affinity = host_affinity

        return self

    def with_libraries(self, libraries):
        # type: (dict) -> JobConfig
        """Sets multiple libraries required by the job.

        See the `JobConfig.libraries` doc for more detail.

        Args:
            libraries (Dict str=str): See `JobConfig.libraries`
        """
        if not isinstance(libraries, dict):
            raise TypeError('libraries must be a dict with format {package_name=package_path}')

        for library_package, library_path in libraries.items():
            self.add_library(library_package, library_path)
        
        return self
    
    def with_capability(self, capability):
        # type: (str) -> JobConfig
        """Specifies a capability required by the job.

        See the `JobConfig.capabilities` doc for more details on capabilities.
        """
        if not isinstance(capability, basestring):
            raise TypeError('capability must a str-like type')

        self.capabilities.append(capability)

        return self

    def add_library(self, library_package, library_path):
        # type: (str) -> JobConfig
        """Specifies a library required by the job.

        See the `JobConfig.libraries` doc for more detail.

        Args:
            library_package (str): The name of the package defined by the library. 
            library_path (str): The local path to the library.
        """
        if not isinstance(library_package, basestring):
            raise TypeError('library_package must a str-like type')

        if not isinstance(library_path, basestring):
            raise TypeError('library_path must a str-like type')

        library_path = os.path.normpath(
            os.path.normcase(
                os.path.abspath(
                    os.path.expanduser(
                        library_path
                    ))))

        if not (os.path.exists(library_path)):
            raise ValueError(library_path + ' not found')

        if not os.path.isdir(library_path):
            raise ValueError(library_path + ' is not a directory')

        self.libraries[library_package] = library_path

        return self

    def _merge_default_dict(self, *source_dicts):
        merged = {}

        for source_dict in source_dicts:
            for key, value in source_dict.items():
                merged[key] = value
        
        return merged


