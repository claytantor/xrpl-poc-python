#!/bin/bash
export API_TIMESTAMP=$(date +%s)
export API_GIT_BRANCH=${CIRCLE_BRANCH:-$(git branch | grep \* | cut -d ' ' -f2)}
export API_GIT_SHA=$(git rev-parse --verify HEAD)
export HTTPD_PROXY_PORT=5005
APP_CONFIG=env/$1/xrpl-poc-python-app.env python -m httpd
