#!/bin/bash
# start the postgres instance
docker run -it --rm -d \
    -p 5432:5432 \
    --network xurlpay \
    --env APP_ENV=local \
    --env POSTGRES_PASSWORD=$1 \
    --env PGDATA=/pgdata \
    -v $(pwd)/pgdata:/pgdata \
    --name xurlpay-postgres-10 \
    postgres:10