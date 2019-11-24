#!/bin/bash

appdir="$(dirname $(readlink -f "$BASH_SOURCE"))"

deactivate

pip3 install -U --user virtualenv

python3 -m virtualenv --python=python3 --no-site-packages "$appdir"

source "$appdir"/bin/activate; pip3 install -U -r "$appdir"/requirements.txt
