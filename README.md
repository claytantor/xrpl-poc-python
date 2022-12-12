# xurlpay.org - a proof of concept for the xurl protocol for durable xumm payloads
A POS (Point of Sale) proof of concept for a new way to do payments for the XRP Ledger API using a proposed protocol called "xurl" which opens up a number of new use cases. 

The xurl protocol is intended to work closely with the [xumm](https://xumm.app) platform. This project is a proof of concept for the xurl protocol, and is not intended for production use but could be uses as a starting point for a production implementation that uses durable payment requests for a Xumm Application.


**Features**

* generation of "scan to pay" invoices that generate xumm payloads
* backend orchestration of xumm payments
* stateful payment requests

This readme is primarily intended to be the project setup playbook for a developer who wants to run a local dev setup, please see the [White Paper](./docs/whitepaper.md) for more information on the technical approach and motivation for this project.

# Configuration
The project is configured using environment variables. The project uses [python-dotenv](https://pypi.org/project/python-dotenv/) to load environment variables from a .env file. The .env file is not checked into the repo, so you will need to create your own. You can use the .env.example file as a template.

```bash
JSON_RPC_URL="https://s.altnet.rippletest.net:51234/"
DATABASE_URL="postgresql://postgres:SooperSecret!@xurlpay-postgres-10:5432/xurlpay"
APP_LOG_LEVEL="DEBUG"
APP_LOG_PATH="/home/foo/logs/xrpl-poc-python-api.log"
API_VERSION="0.1.3"
API_OPENAPI_URL="/openapi.json"
API_ROOT_PATH="/"
API_TOKEN_PATH="/token"
APP_BASEURL_API="http://localhost:5000"
XRP_NETWORK_ENDPOINT="https://s.altnet.rippletest.net:51234/"
XRP_NETWORK_TYPE="testnet"
XRP_NETWORK_EXPLORER="https://testnet.xrpl.org"
XRP_WS_NET="wss://s.altnet.rippletest.net:51233"
XUMM_API_KEY="1b144141-..."
XUMM_API_SECRET="7acffb42-..."
XUMM_APP_DEEPLINK="https://xumm.app/detect/xapp:sandbox.32849dc99872"
AWS_BUCKET_NAME="dev.xurlpay.org"
AWS_UPLOADED_IMAGES_PATH="uploaded_images"
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="Uougc3..."
```
If you want to upload images to AWS S3 you will need to set up an AWS account and create an S3 bucket. You will also need to create an IAM user with access to the bucket. 

## Building And Running The Project
There are a number of ways that someone can build and run the project. You can build and run the project locally, or you can use the docker image. The docker image is intended to be used for local development or deployed in a workload cluster.

### Building and Running Locally
The project is built using python 3.8.5 and pipenv. You can install the dependencies using pipenv and run the project using the pipenv shell.

```bash
pipenv install
pipenv shell
python -m uvicorn app.main:app --reload
```

If you choose to build and run locally you will need to set up a postgres database and configure the app to use it. You can use the a docker instance stand up a postgres database if you wish. You will need to create a database and user for the app to use. You can use the following commands to create the database and user.

[Standing Up a Postgres 10 Database with Docker](./docker/POSTGRES10.md)

## The xurlpay/xurlpay-api docker image as a local dev environment
Its is also possible to run the xurlpay/xurlpay-api docker image locally with a postgres database, and start it up using docker exec.

[The xurlpay/xurlpay/xrplpay-api Docker Image as a Local DEV Environment](./docker/API.md)

