#!/usr/bin/env bash

# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

pypiUsername="__token__"
pypiToken="$1"

python setup.py sdist --dist-dir=dist/pkg
python setup.py bdist_wheel --dist-dir=dist/pkg

twine upload -u "$pypiUsername" -p "$pypiToken" dist/pkg/*