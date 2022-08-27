# xrpl pos
A poc for xrpl pos

# run the flask app
#!/bin/bash
FLASK_APP=api APP_CONFIG=config/local.env flask run  --host=0.0.0.0 --port=5000 --cert=cert.pem --key=key.pem --debugger --reload

# run the cli app
APP_CONFIG=config/local.env python -m api.xrpcli



## signing a message
```APP_CONFIG=config/local.env python -m api.xrpcli -s goodboy -sk EDFCA0B2956D54A4AD70823638E8ADFE6F526AB03FE593E5DC8D46FB692D896E50
message: Z29vZGJveQ== signature: IvFIAA9XxCAuNkUQSHyFTqDWxqme301NRd+VLcoS6mPNdQDjqIe2dsyLGywmaVhavDzHhmo9EhJQz0opjWc3BA==```

## verify a message
```APP_CONFIG=config/local.env python -m api.xrpcli -v Z29vZGJveQ== -pk ED706ED2E4C67EC9603327D46F66DB9CAC999C6AA527FC111C8BC47C74A0BC812C -g IvFIAA9XxCAuNkUQSHyFTqDWxqme301NRd+VLcoS6mPNdQDjqIe2dsyLGywmaVhavDzHhmo9EhJQz0opjWc3BA==
message verified```




# running migrations
FLASK_APP=api APP_CONFIG=config/local.env flask db init

FLASK_APP=api APP_CONFIG=config/local.env flask db migrate

FLASK_APP=api APP_CONFIG=config/local.env flask db upgrade

