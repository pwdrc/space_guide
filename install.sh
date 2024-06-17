#!/bin/bash

# criar .venv
python3 -m venv .venv

pip install -r requirements.txt

python setup.py install