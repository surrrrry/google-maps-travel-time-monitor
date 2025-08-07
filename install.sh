#!/usr/bin/env bash

pip3 uninstall template-package -y

python setup.py sdist
pip3 install dist/*.tar.gz --upgrade

rm -r dist
rm -r *.egg-info

