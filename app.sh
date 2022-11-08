#!/bin/bash
# to do mobile testing and https use the certificate
#FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --cert=cert.pem --key=key.pem --debugger --reload

# no cert version
FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --debugger --reload
