#!/bin/bash
# Requirements:
#  - Python 3
#  - pip3 install bandit
# Reference https://github.com/PyCQA/bandit for
# creating a virtual environment instead

PY_FILE="$1"
echo "Running Bandit on $PY_FILE"

bandit -r $PY_FILE > bandit_$PY_FILE.txt

