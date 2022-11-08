#!/bin/bash
# to do mobile testing and https use the certificate
FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --cert=env/local/clay-deeporb-20.local+3.pem --key=env/local/clay-deeporb-20.local+3-key.pem --debugger --reload

