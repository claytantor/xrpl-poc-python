# starting compose


`bash scripts/ops/run_compose.sh prd <KEY> <SECRET>`


**building the docker image**

```bash
docker build -t xrpl-poc-python-app .
```
the docker image is also built using the .circleci/config.yml configuration file.


## deployment to an environment



**deploying the react app**
The react app will use aws cli to deploy to the cloudfront.

```bash
npm run deploy-prd
```

