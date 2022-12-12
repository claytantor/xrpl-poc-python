# The xurlpay/xurlpay/xrplpay-api Docker Image as a Local DEV Environment
This is the developer documentation for running the xurlpay/xurlpay/xrplpay-api docker image locally with a postgres database, and loading it with some base data. Please see the top level README.md for more information on how to build and run the project.

NOTE: This is a work in progress. We are still working out the permissions on the pgdata dir so that the docker container can write to it. For now, we just set the permissions to 777. We are also working out the best way to load the base data into the database, and how to run the database in a docker container.

## Staging Database and Loading Base Data
Startup a postgres instance pointing to the data dir as a volume. You will want to create a new data dir for each instance you run.

[Standing Up a Postgres 10 Database with Docker](./POSTGRES10.md)


## Standing up the xurlpay API
Now that the database is running, we can stand up the xurlpay API. We will use the docker image that we built in the top level README.md.

### Building the app docker image
Note: we need to still work out the permissions on the pgdata dir so that the docker container can write to it. For now, we just set the permissions to 777.

```
sudo chmod -R guo+rwx pgdata/
TS=$(date +%s) \
docker build -f docker/Dockerfile.app \
    --build-arg BUILD_TS=$TS \
    --build-arg APP_CONFIG="/env/xrpl-poc-python-app.env" \
    -t xurlpay/xrplpay-api:latest .
```

### Run the docker image for the xurlpay API

```
docker run -it --rm \
    -p 5000:5000 \
    --network xurlpay \
    -v $(pwd)/env/local_docker:/env \
    -v $(pwd)/data:/data \
    --name xurlpay-api \
    xurlpay/xrplpay-api:latest
```

### Test that the API is running
`curl http://localhost:5000/info`

should return:

```json
{
    "version":"0.1.3",
    "commit_sha":"1d688d0124f0673864d47d92b669ce8d36126524",
    "api_branch":"uvicorn-base"}    
```

### Access to swagger docs
[http://localhost:5000/docs](http://localhost:5000/docs)


### You can now use the token path to get a token

```bash
curl 'http://localhost:5000/token' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Authorization: Basic Og==' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: http://localhost:5000' \
  -H 'Referer: http://localhost:5000/docs' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'grant_type=password&username=rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y&password=secret' \
  --compressed
```

response:

```json
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGNFdksydnVXTnc1bXZtM0pRb3RHNnNpTXcxaUdkZTFZIiwibmV0Ijoid3NzOi8vcy5hbHRuZXQucmlwcGxldGVzdC5uZXQ6NTEyMzMifQ.aPBsPJgAZLmwZHUwMGAucD827Byco57Zoq6L9tPbWsg"}

```

You can also use the swagger UI to get a token:
[http://localhost:5000/docs](http://localhost:5000/docs)


username: rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y
password: secret

```
Scopes are used to grant an application different levels of access to data on behalf of the end user. Each API may declare one or more scopes.

API requires the following scopes. Select which ones you want to grant to Swagger UI.

OAuth2PasswordBearer (OAuth2, password)
Authorized
Token URL: /token

Flow: password

username: rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y
password: ******
Client credentials location: basic
client_secret: ******
```

Once you have a token, you can use it to access the protected endpoints.
