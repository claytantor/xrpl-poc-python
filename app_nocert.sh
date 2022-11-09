#!/bin/bash
# to do mobile testing and https use the certificate
RUN_ENV=$1
FLASK_APP=api APP_CONFIG=env/$RUN_ENV/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --debugger --reload

