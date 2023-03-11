#!/usr/bin/env bash

python3 -m flask db upgrade
flask create-admin
flask run --host=0.0.0.0