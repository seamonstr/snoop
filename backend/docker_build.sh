#!/bin/bash

set -e

poetry build -f sdist
poetry export -f requirements.txt -o dist/requirements.txt
cp docker/* settings.toml logging*.cfg dist 
cd dist

TARBALL=$(ls backend-?.?.?.tar.gz)
docker build --build-arg BACKEND_TGZ=${TARBALL} --tag snoop-backend .
