#!/bin/bash
echo ""
echo "loading env vars"
export $(grep -v '^#' .env | xargs -0)

echo ""
echo "building docker image"
docker build -t $CONTAINER_NAME .

echo ""
echo "running container"
docker run --rm --env-file=".env" -e "TOKEN=${TEST_TOKEN}" -e "PORT=80" -p $PORT:80 $CONTAINER_NAME
