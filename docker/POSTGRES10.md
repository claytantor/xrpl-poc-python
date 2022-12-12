# Standing Up a Postgres 10 Database with Docker
This is the developer documentation for running the xurlpay/xrpl-postgres-10 docker image locally with a postgres database, and loading it with some base data. Please see the top level README.md for more information on how to build and run the project.

NOTE: This is a work in progress. We are still working out the permissions on the pgdata dir so that the docker container can write to it. For now, we just set the permissions to 777. We are also working out the best way to load the base data into the database, and how to run the database in a docker container.

## Staging Database and Loading Base Data 
Startup a postgres instance pointing to the data dir as a volume. You will want to create a new data dir for each instance you run.

```bash
# setup the data dir
mkdir -p pgdata
sudo chmod -R guo+wrx pgdata

# create the docker network
docker network create xurlpay

# start the postgres instance
docker run -it --rm \
    -p 5432:5432 \
    --network xurlpay \
    --env APP_ENV=local \
    --env POSTGRES_PASSWORD=SooperSecret! \
    --env PGDATA=/pgdata \
    -v $(pwd)/pgdata:/pgdata \
    --name xurlpay-postgres-10 \
    postgres:10


PostgreSQL init process complete; ready for start up.

2022-12-11 23:01:01.705 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2022-12-11 23:01:01.705 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2022-12-11 23:01:01.709 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2022-12-11 23:01:01.723 UTC [68] LOG:  database system was shut down at 2022-12-11 23:01:01 UTC
2022-12-11 23:01:01.727 UTC [1] LOG:  database system is ready to accept connections

```

You should be able to see the docker containers running

```bash
$ docker ps

CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
c77adf723174   postgres:10                      "docker-entrypoint.s…"   47 seconds ago   Up 46 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   xurlpay-postgres-10
```

### Create the database
```bash
docker exec -it xurlpay-postgres-10 psql -U postgres

```

and 

```postgresql
postgres=# CREATE DATABASE xurlpay;
CREATE DATABASE
postgres=# \q
```

### Loading the base data into postgres
1. Run the api container to load the base schema into the database.
2. Run the load command to load the base data into the database.

Note: we need to still work out the permissions on the pgdata dir so that the docker container can write to it. For now, we just set the permissions to 777.

```bash
sudo cp data/xurlpay_base_data.sql pgdata/.
sudo chmod -R guo+rwx pgdata/
docker exec -it xurlpay-postgres-10 bash
psql -U postgres xurlpay < /pgdata/xurlpay_base_data.sql
```
