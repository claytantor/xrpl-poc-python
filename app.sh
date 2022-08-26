#!/bin/bash
FLASK_APP=api APP_CONFIG=config/local.env flask run  --host=0.0.0.0 --port=5000 --cert=cert.pem --key=key.pem --debugger --reload
