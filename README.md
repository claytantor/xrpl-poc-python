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



(xrpl) (base) clay@orion-lap:~/data/github.com/claytantor/xrpl-poc-python/webapp$ curl 'https://localhost:5000/wallet'   -H 'sec-ch-ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"'   -H 'Accept: application/json, text/plain, */*'   -H 'Content-Type: application/json'   -H 'Referer: https://localhost:3001/'   -H 'sec-ch-ua-mobile: ?0'   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'   -H 'sec-ch-ua-platform: "Linux"'   --data-raw '{"headers":{"Accept":"*/*","Content-Type":"application/json"},"data":{}}'   --compressed -k
{"account_info":{"account_data":{"Account":"rPfFWRTn1gLzvghfv3MjvTvtNraoWhv42c","Balance":"1000000000","Flags":0,"LedgerEntryType":"AccountRoot","OwnerCount":0,"PreviousTxnID":"3B421C2EAD8C6CD7945403D4034E3304BB46595C0BEB04074B4BA9D4C4E05F2E","PreviousTxnLgrSeq":32650027,"Sequence":32650027,"index":"16D0BD1E7C2B0E7D37DE63C05A0550A0BB8A700FB6DBC09E36597AAE45609B56"},"ledger_current_index":32650029,"queue_data":{"txn_count":0},"validated":false},"classic_address":"rPfFWRTn1gLzvghfv3MjvTvtNraoWhv42c","private_key":"ED8FA5B9C31B340E40029F0B413F438EB160EB318A0A4E24A3F84B034CD4D4819F","public_key":"EDFACCF19C054522BAE948BB4ED3C0C0050917A9A7FEB3C20EB3E78B3D8671F87C","seed":"sEdSb7wrzyy3xBNgre6rKSDAbV9wW4n"}


Wallet created. Save this info now!
classic address
rBEybSc8wps5gSUnr5ZimYrjcQDKUfubTG
private key
ED41CD44DB572247F931F8EC0EB75CD58419D7348D380F8E8168591A30DB5AB3FD
public key
ED48E6400384A639B33761CB76FCE434D9FB8A20D4600C709B00E33D6757E05DE7
seed
sEdTMVSRi37P7jHeMp93sv2y9Dv1cSU
