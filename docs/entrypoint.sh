#!/usr/bin/env bash

# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

pip install --user -r /app/requirements.txt

if [ "$1" == "dev" ]; then
    watch -d pdoc -c show_source_code=False -o dist --html -f --template-dir /app/docs/pdoc_template/ aegisblade
else
    pdoc -c show_source_code=False -o dist --html -f --template-dir /app/docs/pdoc_template/ aegisblade
fi