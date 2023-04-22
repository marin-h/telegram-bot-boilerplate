#!/bin/bash
pwd 
echo "cleaning env.."
killall ngrok > /dev/null
docker stop $(docker ps -aq) > /dev/null
docker rm $(docker ps -aq) > /dev/null

echo ""
echo "loading env vars"
export $(grep -v '^#' .env | xargs -0)

echo ""
echo "building docker image"
docker build -t mate-bot .

echo ""
echo "running app container"
docker run -d --env-file=".env" -e "TOKEN=${TEST_TOKEN}" -e "BOT_ENV=staging" -e "PORT=80" -e "CONFIG_FOLDER_ID=${STAGING_CONFIG_FOLDER_ID}" -e GOOGLE_SERVICE_ACCOUNT_CREDENTIALS=${STAGING_GOOGLE_CREDENTIALS} -p $PORT:80 mate-bot

sleep 2

echo ""
echo "running ngrok container"
docker run -d --net=host -it -e "NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}" ngrok/ngrok:2.3.40-alpine http "$PORT" --log=stdout

echo "waiting for ngrok api"
while [ -z "$WEBHOOK" ]
do
    echo "webhook not ready, retrying..."
    sleep 3
    WEBHOOK=$(curl -s "localhost:4040/api/tunnels" -H "Content-type: application/json" | jq -r '.tunnels[] | select(.name=="command_line").public_url')
done

echo ""
echo "Ngrok is at $WEBHOOK"
echo ""

echo ""
echo "setting webhook: curl https://api.telegram.org/bot$TEST_TOKEN/setWebHook?url=$WEBHOOK"
curl -s "https://api.telegram.org/bot$TEST_TOKEN/setWebHook?url=$WEBHOOK" | jq .

echo ""
echo "getting webhook info: curl https://api.telegram.org/bot$TEST_TOKEN/getWebhookInfo"
curl -s "https://api.telegram.org/bot$TEST_TOKEN/getWebhookInfo" | jq . 

echo ""
echo "Check localhost:4040 for ngrok status page, and tail ngrok.logs file for logs."
