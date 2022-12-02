#!/bin/bash

ENV=$1
BASE_DIR=$(pwd)
echo "BASE_DIR: $BASE_DIR"

# data directory
DATA_DIR=$BASE_DIR/data
echo "DATA_DIR: $DATA_DIR"
if [ ! -d $DATA_DIR ]; then
  echo "$DATA_DIR does not exist."
  mkdir $DATA_DIR
fi

# env
ENV_DIR=$DATA_DIR/$ENV/$1
echo "ENV_DIR: $ENV_DIR"
if [ ! -d "$BASE_DIR/env" ]; then
  echo "$BASE_DIR/env does not exist."
  mkdir $BASE_DIR/env
  mkdir $BASE_DIR/env/$ENV 
  cp -r $BASE_DIR/cicd/env/xrpl-poc-python-app-example.env $BASE_DIR/env/$ENV/xrpl-poc-python-app.env
fi