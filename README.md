# Teuthology API

A REST API to execute [teuthology commands](https://docs.ceph.com/projects/teuthology/en/latest/commands/list.html). 

## Setup

#### Option 1: (teuthology docker setup)

1. Clone [teuthology](https://github.com/ceph/teuthology) and [teuthology-api](https://github.com/VallariAg/teuthology-api).
2. Rename `.env.dev` file to `.env`. 
3. Configure secrets:
    
   3.1. Create a Github OAuth Application by following [these](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) instructions. Set "Homepage URL" as `http://localhost:8082/` and "Authorization callback URL" as `http://localhost:8082/login/callback/`. 

   3.2. Ensure [ceph](https://github.com/ceph) belongs in your public list of organizations[[ref](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-membership-in-organizations/about-organization-membership)]. By default your membership is set private, change that to public by following [these](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-membership-in-organizations/publicizing-or-hiding-organization-membership) steps.

   3.3. Save `CLIENT_ID` and `CLIENT_SECRET` from your Github OAuth App to your local `.env` file as `GH_CLIENT_ID` and `GH_CLIENT_SECRET`.

4. Add the following to [teuthology's docker-compose](https://github.com/ceph/teuthology/blob/main/docs/docker-compose/docker-compose.yml) services.
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
5. Follow teuthology development setup instructions from [here](https://github.com/ceph/teuthology/tree/main/docs/docker-compose).

## Documentation

The documentation can be accessed at http://localhost:8082/docs after running the application.

Note: To run commands, authenticate by visiting `http://localhost:8082/login` through browser and follow the github authentication steps (this stores the auth token in browser cookies). 

### Route `/`

```
curl http://localhost:8082/
```
Returns `{"root": "success", "session": { <authentication details> }}`.

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

## GSOC/OUTREACHY 2023

This section is for GSOC/OUTREACHY 2023 applicants.

### Task 1: Run Teuthology & Teuthology-API
Install Teutholology-API by following the instructions above. Make sure to get all the containers running with healthy status and take a screen shot of all the running containers. TIP: In https://github.com/ceph/teuthology/tree/main/docs/docker-compose#readme run TEUTHOLOGY_WAIT=1 ./start.sh so you have time to take screen shots. Submit the screenshots to all your mentors through email.

### Task 2: Add unit-test to suite & kill route
Add unit-tests for 2 functions of your choice, 1 in `src/services/suite.py` and 1 in `src/services/kill.py.` You should be using `TestClient` library from fast-api, following this [doc](https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file).

File a PR tagging the `gsoc-outreachy` label, please use `git commit -s` to sign your commits.

### Task 3: Create a low fidelity UX/UI mockup 
The purpose of this project is to enable Teuthology to schedule/kill jobs
through [Pulpito](https://pulpito.ceph.com/), therefore, we need to also add a new
widget, e.g., action bar -> form that allows you to schedule jobs, delete button on each runs/jobs. Please submit the mockup by filing a PR to this repo. This task is open-ende so feel free to use any tools (you can even hand draw it).

Again, please use the `gsoc-outreachy` label and `git commit -s` to sign your commits.