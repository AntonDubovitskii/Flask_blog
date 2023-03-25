#!/usr/bin/env bash

python3 -m flask db upgrade
flask create-admin
flask create-tags
flask run --host=0.0.0.0