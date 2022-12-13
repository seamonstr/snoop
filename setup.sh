#!/bin/bash

set -e

npm install
npx mookme init --only-hook --skip-types-selection
