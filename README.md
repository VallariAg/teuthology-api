# Teuthology API

A REST API to execute [teuthology commands](https://docs.ceph.com/projects/teuthology/en/latest/commands/list.html). 

## Setup

#### With teuthology's docker setup 

1. Install [docker](https://docs.docker.com/get-docker/).
2. Clone [teuthology](https://github.com/ceph/teuthology) and [teuthology-api](https://github.com/VallariAg/teuthology-api) in a common directory, i.e `/path/to/dir/teuthology` and `path/to/dir/teuthology-api`.
3. Add the following to [teuthology's docker-compose](https://github.com/ceph/teuthology/blob/main/docs/docker-compose/docker-compose.yml) services.
    ```
    teuthology_api:
        build:
          context: ../../../teuthology-api
        ports:
            - 8082:8082
        depends_on:
            - teuthology
            - paddles
        links:
            - teuthology
            - paddles
    ```
4. Follow teuthology development setup instructions from [here](https://github.com/ceph/teuthology/tree/main/docs/docker-compose).


For development setup, you can:
1. In teuthology-api's Dockerfile, instead of gunicorn use entrypoint as `ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--port", "8082", "--host", "0.0.0.0"]` to restart app on changes.
2. In teuthology_api's docker-compose setup, mount host directory to docker's directory with: `volumes: ../../../teuthology-api:/teuthology_api/:rw`


## Documentation

The documentation can be accessed at http://localhost:8082/docs after running the application.

### Route `/`

```
curl http://localhost:8082/
```
Returns `{"root": "success"}`.

### Route `/suite`

POST `/suite/`: schedules a run.
Example:
```
curl --location --request POST 'http://localhost:8082/suite/' \
--header 'Content-Type: application/json' \
--data-raw '{
         "--ceph": "main",
         "--ceph-repo": "https://github.com/ceph/ceph-ci.git",
         "--limit": "2",
         "--newest": "0",
         "--machine-type": "testnode",
         "--num": "1",
         "--priority": "150",
         "--suite": "teuthology:no-ceph",
         "--suite-branch": "main",
         "--suite-repo": "https://github.com/ceph/ceph-ci.git",
         "--teuthology-branch": "main",
         "--verbose": "1",
         "--user": "vallariag"
 }'
```


## Troubleshooting


1. If `paddles` container is unhealthy and it's logs say:
`(psycopg2.errors.InsufficientPrivilege) permission denied for schema public`

    Then, follow these steps and restart paddles container:
    ```
    $ docker exec -it <paddles container id> sh
    > psql
    > GRANT ALL ON DATABASE paddles TO admin;
    > ALTER DATABASE paddles OWNER TO admin;
    ```



