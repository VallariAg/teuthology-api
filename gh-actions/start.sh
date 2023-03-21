#!/bin/bash
set -e
folder="teuthology"
if [ ! -d "$folder" ] ; then
    git clone https://github.com/ceph/teuthology.git
    echo "  teuthology_api:
        build:
            context: ../../../../
        ports:
            - 8082:8082
        depends_on:
            - teuthology
            - paddles
        links:
            - teuthology
            - paddles
    " >> teuthology/docs/docker-compose/docker-compose.yml
fi
cd teuthology/docs/docker-compose
./start.sh