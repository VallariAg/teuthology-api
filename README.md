# Teuthology API

A REST API to execute [teuthology commands](https://docs.ceph.com/projects/teuthology/en/latest/commands/list.html). 

## Setup

#### Option 1: (teuthology docker setup)

1. Clone [teuthology](https://github.com/ceph/teuthology) and [teuthology-api](https://github.com/VallariAg/teuthology-api).
2. Add the following to [teuthology's docker-compose](https://github.com/ceph/teuthology/blob/main/docs/docker-compose/docker-compose.yml) services.
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
3. Follow teuthology development setup instructions from [here](https://github.com/ceph/teuthology/tree/main/docs/docker-compose).

## Documentation

The documentation can be accessed at http://localhost:8082/docs after running the application.

### Route `/`

```
curl http://localhost:8082/
```
Returns `{"root": "success"}`.

### Route `/suite`

POST `/suite/`: schedules a run.

Two query parameters: 
- `dry_run` (boolean) - Do a dry run; do not schedule anything.
- `logs` (boolean) - Send scheduling logs in response.

Example:
```
curl --location --request POST 'http://localhost:8082/suite?dry_run=false&logs=true' \
--header 'Content-Type: application/json' \
--data-raw '{
         "--ceph": "wip-dis-testing-2",
         "--ceph-repo": "https://github.com/ceph/ceph-ci.git",
         "--kernel": "distro",
         "--limit": "2",
         "--newest": "0",
         "--machine-type": "testnode",
         "--num": "1",
         "--priority": "70",
         "--suite": "teuthology:no-ceph",
         "--suite-branch": "wip-dis-testing-2",
         "--suite-repo": "https://github.com/ceph/ceph-ci.git",
         "--teuthology-branch": "main",
         "--verbose": "1",
         "--user": "vallariag"
 }'
```

