#!/bin/bash

appdir="$(dirname $(readlink -f $BASH_SOURCE))"

pip3 install -U --user virtualenv

virtualenv --python=python3.7 --no-site-packages $appdir

source $appdir/bin/activate; pip install -r $appdir/requirements.txt


