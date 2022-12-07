#!/bin/bash
# to do mobile testing and https use the certificate
FLASK_APP=api APP_CONFIG=env/$1/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --debugger --reload

