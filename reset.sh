#!/bin/bash

docker compose -f ./test-docker-compose.yml down &&
docker image rm vision:test &&
docker image rm alpine-mongo:test &&
docker volume prune &&
docker volume rm vision_vision_vol
