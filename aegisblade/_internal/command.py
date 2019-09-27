# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import subprocess

from typing import List


class Command(object):
    """Internal class for executing Processes"""
    executable = None
    arguments = None

    def __init__(self, executable, arguments):
        # type: (str, List[str]) -> None
        self.executable = executable
        self.arguments = arguments

        self.environment_variables = dict()

    def environment(self, key, value):
        self.environment_variables[key] = value
        return self

    def environment_dict(self, env_dict):
        for key, value in env_dict.items():
            self.environment_variables[key] = value
        return self

    def execute(self):
        s_process_args = [self.executable]
        s_process_args.extend(self.arguments)

        s_process = subprocess.Popen(
            s_process_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.environment_variables,
            universal_newlines=True)

        out, err = s_process.communicate()
        exitcode = s_process.returncode

        # print out
        # print err

        return ProcessResult(self, out, err, exitcode)


class ProcessResult():
    """
    :type process: Command
    :type s_process: subprocess.Popen
    :type stdout: str
    :type std
    """

    def __init__(self, process, stdout, stderr, exitcode):
        self.process = process
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode

    def failed(self):
        return self.exitcode != 0
