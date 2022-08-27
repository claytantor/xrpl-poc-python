#!/usr/bin/env bash
export ENV=$1
if [ "$ENV" = "local" ]; then 
    export BRANCH_TAG="local"
    echo "ENV: $ENV BRANCH_TAG: $BRANCH_TAG"
fi

if [ "$ENV" = "dev" ]; then
    
    export BRANCH_TAG="dev"
    echo "ENV: $ENV BRANCH_TAG: $BRANCH_TAG"
fi

if [ "$ENV" = "prd" ]; then
    export BRANCH_TAG="main"
    echo "ENV: $ENV BRANCH_TAG: $BRANCH_TAG"
fi

echo "FINAL ENV: $ENV BRANCH_TAG: $BRANCH_TAG"
export PROJECT_NAME="xrpl-poc-python"
export DEVOPS_BASEDIR=$(pwd)
export AWS_ACCESS_KEY_ID=$2
export AWS_SECRET_ACCESS_KEY=$3
export ETL_LOCAL=$(pwd)/etl
export ETL_HOME=/etl

# cleanup previous deployments
# docker system prune -a -f

# login to docker
aws ecr get-login-password \
    --region us-west-2 \
| docker login \
    --username AWS \
    --password-stdin 705212546939.dkr.ecr.us-west-2.amazonaws.com

docker pull 705212546939.dkr.ecr.us-west-2.amazonaws.com/claytantor/$PROJECT_NAME:$BRANCH_TAG

docker-compose -f $DEVOPS_BASEDIR/devops/compose/docker-compose.yml --env-file env/$ENV/xrpl-poc-python-app.env pull
docker-compose -f $DEVOPS_BASEDIR/devops/compose/docker-compose.yml --env-file env/$ENV/xrpl-poc-python-app.env up -d
