#!/usr/bin/env bash

python3 -m flask db upgrade
flask init-db
flask create-users
flask create-articles
flask run --host=0.0.0.0