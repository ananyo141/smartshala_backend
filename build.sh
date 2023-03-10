#!/usr/bin/env bash

# exit on error
set -o errexit

pip install --upgrade poetry
poetry install

poetry run ./manage.py collectstatic --no-input
poetry run ./manage.py makemigrations smartshala
poetry run ./manage.py migrate
