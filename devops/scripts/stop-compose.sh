#!/usr/bin/env bash
export ENV=$1
export DEVOPS_BASEDIR=$(pwd)/devops
docker-compose -f $DEVOPS_BASEDIR/compose/docker-compose.yml --env-file env/$ENV/xrpl-poc-python-app.env down
docker image prune -a -f
