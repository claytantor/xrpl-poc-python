# xurlpay.org - a proof of concept for the xurl protocol
A POS (Point of Sale) proof of concept for a new way to do payments for the XRP Ledger API using a proposed protocol called "xurl" which opens up a number of new use cases.

**Features**

* generation of "scan to pay" invoices
* generation of payment memos
* stateful payment requests

This readme is primarily intended to be the project setup playbook for a developer who wants to run a local dev setup, please see the [White Paper](./docs/whitepaper.md) for more information on the technical approach and motivation for this project.

## Local Setup

### environment variables
environment variables are used to configure the application and can contain secrets, for that reason they are not included in the repository.

**example**

```bash
JSON_RPC_URL="https://s.altnet.rippletest.net:51234/"
WALLET_ADDRESS_R="rU32wptoF4YPK3USvuYipUeDMqjF371B9J"
WALLET_SECRET_R="<secret>"
DATABASE_URL="sqlite:////data/xurl.db"
APP_LOG_LEVEL="DEBUG"
```

### run the cli app
`APP_CONFIG=env/local/xrpl-poc-python-app.env python -m api.xrpcli`

**signing a message**

`APP_CONFIG=env/local/xrpl-poc-python-app.env python -m api.xrpcli -s goodboy -sk EDFCA0B2956D54A4AD70823638E8ADFE6F5SOOPERSECRET5DC8D46FB692D896E50
message: Z29vZGJveQ== signature: IvFIAA9XxCAuNkUQSHyFTqDWxqme301NRd+VLcoS6mPNdQDjqIe2dsyLGywmaVhavDzHhmo9EhJQz0opjWc3BA==`

**verify a message**

`APP_CONFIG=env/local/xrpl-poc-python-app.env python -m api.xrpcli -v Z29vZGJveQ== -pk ED706ED2E4C67EC9603327D46F66DB9CAC999C6AA527FC111C8BC47C74A0BC812C -g IvFIAA9XxCAuNkUQSHyFTqDWxqme301NRd+VLcoS6mPNdQDjqIe2dsyLGywmaVhavDzHhmo9EhJQz0opjWc3BA==
message verified`

### running the flask app

**local deployment**
Local deployment has two components:

1. The flask app (deployed and fronted as the API in AWS API Gateway)
2. The xrpcli react app (deployed and fronted as a Cloudfront edge using the awscli)

A [script is provided](./app.sh) to start the flask app, or you can just start the flask app directly.

**running the flask app**

```bash
#!/bin/bash
FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask run  --host=0.0.0.0 --port=5000 --cert=cert.pem --key=key.pem --debugger --reload
```

**migrations**
```
FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask db init

FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask db migrate

FLASK_APP=api APP_CONFIG=env/local/xrpl-poc-python-app.env flask db upgrade
```


### running client react app
The client react app is intended deployed as a react app that talks to the API. Its in the [webapp](./webapp) directory and you will need to work from there when trying to run locally.

**getting the react app installs**

```bash
cd ./webapp
npm install
```

**running the react app**

There is a little bit of scripting that runs included when you want to run local.

```bash
npm run serve-local
```

This will start the react app with the local deployment configuration and use the certs and keys in the local directory so it runs under https. Since this is a self signed certificate you will need to tell the browser its ok to proceed.

[https://localhost:3001/](https://localhost:3001/)

## generating certs and keys for flask app

```bash
sudo apt install libnss3-tools -y
sudo apt install openssl -y

wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
sudo cp mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert
sudo chmod +x /usr/local/bin/mkcert

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=US/ST=Oregon/L=Portland/O=XurlPay.org/CN=dev-xurlpay.org"

```

# rsync to ec2 instance

```bash
bash cicd/sh/rsync-api.sh
```

# xApp webhook response

```json
{
    "meta": {
        "url": "https://devapi.xurlpay.org/v1/xumm/webhook",
        "application_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
        "payload_uuidv4": "a44e2edf-563f-4c59-b551-4b442a009477",
        "opened_by_deeplink": false
    },
    "custom_meta": {
        "identifier": null,
        "blob": null,
        "instruction": null
    },
    "payloadResponse": {
        "payload_uuidv4": "a44e2edf-563f-4c59-b551-4b442a009477",
        "reference_call_uuidv4": "b608d181-520f-4282-a0bd-6e6e7de7d14d",
        "signed": true,
        "user_token": true,
        "return_url": {
            "app": null,
            "web": null
        },
        "txid": "336EFE27BEB7B494150D9DB7C59F8AA6AD3FDDE4E2AC51364797C9EBEF0BD599"
    },
    "userToken": {
        "user_token": "4de21968-8c2f-4fb3-9bb6-94b589a13a8c",
        "token_issued": 1667957297,
        "token_expiration": 1670553892
    }
}
```


https://dev.xurlpay.org/api/xumm/deeplink?classic_address=rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y&amount=9.25

https://devapi.xurlpay.org/v1/xumm/deeplink?classic_address=rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y&amount=9.25


`https://devapi.xurlpay.org/v1/xumm/deeplink?classic_address=rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y&amount=9.25` and it redirects to my xApp as `https://xumm.app/detect/xapp:sandbox.32849dc99872?amount={amount}&memo={memo}&classic_address={classic_address}` but when it comes back to my server the params have been stripped: `<Request 'http://ec2-34-211-56-213.us-west-2.compute.amazonaws.com:5000/xumm/app?xAppStyle=LIGHT&xAppToken=4dc0be9a-922b-4665-97d7-1c1fa73e76fc' [GET]` 


#  running the app

`APP_CONFIG=env/local/xrpl-poc-python-app.env python -m api`

# migrations
APP_CONFIG=env/local/xrpl-poc-python-app.env alembic -c migrations/alembic.ini upgrade head


PYTHONPATH=$(pwd)/api:$PYTHONPATH APP_CONFIG=env/local/xrpl-poc-python-app.env  alembic -c migrations/alembic.ini upgrade head

PYTHONPATH=$(pwd)/api:$PYTHONPATH APP_CONFIG=env/local/xrpl-poc-python-app.env  alembic -c migrations/alembic.ini current