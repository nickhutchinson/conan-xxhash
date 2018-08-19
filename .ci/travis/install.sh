#!/bin/bash
set -euo pipefail
set -x

python2 -m pip install virtualenv --upgrade
virtualenv ~/venv-conan

~/venv-conan/bin/python -m pip install \
    conan \
    conan_package_tools

~/venv-conan/bin/conan user
