#!/bin/sh

virtualenv -p /usr/bin/python3 django_venv
source django_venv/bin/activate
pip3 install -r requirements.txt
