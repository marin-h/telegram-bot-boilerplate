#!/bin/bash

echo ""
echo "loading env vars"
set -a
source <(cat .env | \
    sed -e '/^#/d;/^\s*\$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +a

docker stop matebot > /dev/null
docker rm matebot > /dev/null

echo ""
echo "building docker image"
docker build -t mate-bot .

echo ""
echo "running container"
docker run -d --name matebot --env-file=".env" -e "TOKEN=${TEST_TOKEN}" -e "PORT=$PORT" -p $PORT:80 mate-bot
