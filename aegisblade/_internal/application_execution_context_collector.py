# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import hashlib
import imp
import os
import re
import sys


from aegisblade._internal.atrace import Trace
from aegisblade._internal.application_context_file import ApplicationContextFile
from aegisblade._internal.application_execution_context import ApplicationExecutionContext
from aegisblade._internal.application_package_info import ApplicationPackageInfo
from aegisblade._internal.cached_std_lib_modules import get_std_lib_modules
from aegisblade._internal.command import Command
from aegisblade.__version__ import __version__


class _ApplicationExecutionContextCollector(object):
    """Internal class used to collect the files and data required to 
    build an executable version of this application.
    """

    def collect(self, libraries):
        # type: (dict) -> ApplicationExecutionContext

        pip_packages = self.get_pip_packages(libraries)

        application_execution_context = ApplicationExecutionContext(
            language="python",
            source_runtime_identifier=self.get_platform(),
            target_runtime_name="python",
            target_runtime_version="{0}.{1}".format(sys.version_info.major, sys.version_info.minor),
            packages=pip_packages,
            files=self.get_application_files(
                set([p.name for p in pip_packages]),
                self.get_std_lib_modules(),
                libraries
            ),
            package_manager_source_feeds=[],
            client_version=__version__
        )

        return application_execution_context

    def get_platform(self):
        try:
            import platform
            return platform.platform()
        except:
            return sys.platform

    def get_pip_packages(self, libraries):
        '''
        Get all installed packages (in the current environment)
        '''

        # Workaround for Ubuntu Bug
        # https://stackoverflow.com/questions/39577984/what-is-pkg-resources-0-0-0-in-output-of-pip-freeze-command
        excluded_packages = {'pkg-resources'}

        # Exclude also packages defined in 'libraries'
        for library_package, _ in libraries.items():
            excluded_packages.add(library_package)

        pip_process = Command("pip", ["freeze"]).environment_dict(os.environ).execute()

        pip_packages = []
        for line in pip_process.stdout.split("\n"):
            line = line.strip()
            if line == "":
                continue

            if line.startswith("-e"):
                pip_packages.append(ApplicationPackageInfo(line, None))
            else:
                name, version = line.split("==")

                if name not in excluded_packages:
                    pip_packages.append(ApplicationPackageInfo(name, version))

        return pip_packages

    def get_std_lib_modules(self):
        return get_std_lib_modules()

    def get_application_files(self, pip_package_names, std_library_modules, libraries):
        root_path = self.find_project_root()

        module_conditions = [
            lambda module: 'site-packages' not in module[1],  # Not a site package
            lambda module: not module[0].split('.')[0] in pip_package_names,
            # Not part of an installed package (backup), (optional)
            lambda module: not module[0].split('.')[0] in std_library_modules,
            # Not part of an any stdlib package, (optional)
            lambda module: not module[0] in std_library_modules,  # Not a stdlib package, (optional)
            lambda module: not module[0] in pip_package_names,  # Not a pip package, (optional),
            # lambda module: not module[1].startswith(os.environ.get("VIRTUAL_ENV", None)),
            # Not in the virtual env (some random files)
            lambda module: not '/pycharm.app/' in module[1].lower(),  # Not in pycharm (pycharm debugger),
            lambda module: not module[1].lower().startswith("/system"),   # Not in the OSX system directory
            lambda module: not module[1].lower().startswith("/usr/lib/python")  # Not in Linux Sys directory
        ]

        if os.environ.get("VIRTUAL_ENV", None):
            module_conditions.append(lambda module: not module[1].startswith(os.environ.get("VIRTUAL_ENV")))

        filtered_modules = [m for m in self.get_application_modules() if all(map(lambda condition: condition(m), module_conditions))]

        files = []
        for module in filtered_modules:
            name, path = module
            relative_path_to_root = os.path.relpath(path, root_path)

            if not self.is_subdir(path, root_path):
                found_library = None
                if libraries:
                    for _, library_path in libraries.items():
                        if path.startswith(library_path):
                            Trace.verbose("[INFO] Adding library module to aegisblade_lib {0} ({1})".format(path, library_path))
                            found_library = library_path
                            break

                if found_library:
                    lib_relative_path = os.path.relpath(path, found_library)
                    relative_path_to_root = os.path.join('aegisblade_lib', lib_relative_path)
                else:
                    Trace.verbose("WARNING. Skipping module outside project root directory. ({0})".format(path))
                    continue

            file_contents = None
            with open(path, 'rb') as f:
                file_contents = f.read()

            file_hash = hashlib.sha256()
            file_hash.update(file_contents)
            file_hash = file_hash.hexdigest()

            files.append(ApplicationContextFile(path, relative_path_to_root, file_hash, file_contents, len(file_contents)))

        return files

    def is_subdir(self, test_path, root_path):
        path = os.path.realpath(test_path)
        directory = os.path.realpath(root_path)

        relative = os.path.relpath(path, directory)
        return not (relative == os.pardir or relative.startswith(os.pardir + os.sep))

    def normalize_path(self, path_to_normalize):
        if path_to_normalize is None:
            return None

        normalized_path = os.path.normpath(
            os.path.normcase(
                os.path.abspath(
                    os.path.expanduser(
                        path_to_normalize
                    )
                )
            )
        )

        return normalized_path

    def get_filtered_sys_path(self):
        non_included_paths = []

        python_path = os.path.dirname(sys.executable)
        non_included_paths.append(self.normalize_path(python_path))

        virtual_env_path = os.environ.get("VIRTUAL_ENV", None)
        if virtual_env_path:
            non_included_paths.append(self.normalize_path(virtual_env_path))

        try:
            homebrew_prefix_cmd = Command("brew", ["--prefix"])\
                .environment_dict(os.environ)\
                .execute()

            if not homebrew_prefix_cmd.failed():
                homebrew_prefix = homebrew_prefix_cmd.stdout.replace("\n", "")
                homebrew_path = homebrew_prefix + "/Cellar"
                non_included_paths.append(self.normalize_path(homebrew_path))

        except OSError:
            # Expected on non-mac or non-brew systems
            pass

        path_components = filter(os.path.isdir,
                                map(self.normalize_path,
                                    sys.path[:]))

        for filtered_path in non_included_paths:
            path_components = filter(lambda p: not p.startswith(filtered_path), path_components)

        return path_components

    def get_py_file_suffix_or_none(self, file):
        for suffix in imp.get_suffixes():
            if file[-len(suffix[0]):] == suffix[0]:
                return suffix
        return None

    def get_application_modules(self):
        path = self.get_filtered_sys_path()
        # print("path: " + str(path))

        modules = {}

        for p in path:
            modules.update(self.get_modules_in_directory(p))

        items = list(modules.items())
        items.sort()
        return items

    def get_modules_in_directory(self, directory, d=1):
        # get modules in a given directory
        modules = {}
        for f in os.listdir(directory):
            f = os.path.join(directory, f)
            if os.path.isfile(f):
                m, e = os.path.splitext(f)
                suffix = self.get_py_file_suffix_or_none(f)
                if not suffix:
                    continue
                m = os.path.basename(m)
                if re.compile("(?i)[a-z_]\w*$").match(m):
                    # if suffix[2] == imp.C_EXTENSION:
                    #     # check that this extension can be imported
                    #     try:
                    #         __import__(m)
                    #     except ImportError:
                    #         continue
                    modules[m] = f
            elif os.path.isdir(f):
                m = os.path.basename(f)
                if os.path.isfile(os.path.join(f, "__init__.py")):
                    for mm, f in self.get_modules_in_directory(f, d=d+1).items():
                        modules[m + "." + mm] = f
        return modules

    def find_project_root(self):
        # TODO: Is there a better choice than CWD?
        return self.normalize_path(os.getcwd())
