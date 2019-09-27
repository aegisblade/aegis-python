#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

import os

from setuptools import find_packages
from setuptools import setup


this_file_dir = os.path.dirname(
    os.path.abspath(
        os.path.realpath(__file__)))


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='aegisblade',
    version=find_version(this_file_dir, "aegisblade", "__version__.py"),
    license='LGPL2.1',
    description='Deploy & run your code in a single function call.',

    long_description=read(os.path.join(this_file_dir, "README.md")),
    long_description_content_type='text/markdown',

    author='AegisBlade',
    author_email='welovedevs@aegisblade.com',

    url='https://www.aegisblade.com/',
    project_urls={
        'Github': 'https://github.com/aegisblade/aegis-python',
        'Bug Reports': 'https://github.com/aegisblade/aegis-python/issues',
        'Docs': 'https://www.aegisblade.com/docs',
        'Reference': 'https://www.aegisblade.com/docs/reference/python'
    },

    install_requires=[
        'requests==2.20.1', 'typing==3.6.4', 'cloudpickle==1.2.2'
    ],

    python_requires=">=2.7",

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='aegisblade server aws ec2 devops infrastructure as code IaC serverless kubernetes',
)