#!/usr/bin/env bash

pip install --user -r /app/requirements.txt

if [ "$1" == "dev" ]; then
    watch -d pdoc -c show_source_code=False -o dist --html -f --template-dir /app/docs/pdoc_template/ aegisblade
else
    pdoc -c show_source_code=False -o dist --html -f --template-dir /app/docs/pdoc_template/ aegisblade
fi