#!/bin/bash

echo ""
echo "loading env vars"
set -a
source <(cat .env | \
    sed -e '/^#/d;/^\s*\$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +a

docker stop $(docker ps -aq) > /dev/null
docker rm $(docker ps -aq) > /dev/null

echo ""
echo "building docker image"
docker build -t mate-bot .

echo ""
echo "running container"
docker run --env-file=".env" -e "TOKEN=${TEST_TOKEN}" -e "PORT=80" -p 80:80 mate-bot &
