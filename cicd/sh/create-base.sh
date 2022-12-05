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
ENV_DIR=$DATA_DIR/env/$ENV
echo "ENV_DIR: $ENV_DIR"
if [ ! -d "$BASE_DIR/env" ]; then
  echo "$BASE_DIR/env does not exist."
  mkdir $BASE_DIR/env
  mkdir $BASE_DIR/env/$ENV 
  cp -r $BASE_DIR/cicd/config/xrpl-poc-python-app-example.env $BASE_DIR/env/$ENV/xrpl-poc-python-app.env
fi

# logs
LOGS_DIR=$BASE_DIR/logs
echo "LOGS_DIR: $LOGS_DIR"
if [ ! -d $LOGS_DIR ]; then
  echo "$LOGS_DIR does not exist."
  mkdir $LOGS_DIR
fi

python -m pip install --upgrade pip
pip install -r requirements.txt 

# this omits the qr code lib which 
wget https://github.com/lincolnloop/python-qrcode/archive/refs/tags/v7.3.1.tar.gz
tar -xvf v7.3.1.tar.gz
cd python-qrcode-7.3.1
python setup.py install
cd ..
rm -rf python-qrcode-7.3.1