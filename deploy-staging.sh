#!/bin/bash
term() {
    echo "Stopping container. Cleaning up..."
    docker stop $CONTAINER_NAME > /dev/null 2>&1
    echo bye!
}

trap term SIGINT

echo ""
echo "loading env vars"
export $(grep -v '^#' .env | xargs -0)

echo ""
echo "building docker image"
docker build -t $CONTAINER_NAME .

echo ""
echo "running container"
docker run --rm --env-file=".env" -e "TOKEN=${TEST_TOKEN}" -e "PORT=80" -p $PORT:80 $CONTAINER_NAME &

echo ""
echo "ngrok log dir: ${LOG_DIR}/ngrok.log"
mkdir -p ${LOG_DIR}
touch ${LOG_DIR}/ngrok.log

echo ""
echo "launching ngrok"
ngrok http $PORT -host-header=test.app -log=stdout >> logs/ngrok.log &
pid=$!

sleep 2
WEBHOOK=$(curl -s "localhost:4040/api/tunnels" | jq -r '.tunnels[] | select(.name=="command_line").public_url')

echo ""
echo "Ngrok is at $WEBHOOK"
echo ""

echo ""
echo "setting webhook: curl https://api.telegram.org/bot\$TEST_TOKEN/setWebHook?url=$WEBHOOK"
curl -s "https://api.telegram.org/bot$TEST_TOKEN/setWebHook?url=$WEBHOOK" | jq .

echo ""
echo "getting webhook info: curl https://api.telegram.org/bot\$TEST_TOKEN/getWebhookInfo"
curl -s "https://api.telegram.org/bot$TEST_TOKEN/getWebhookInfo" | jq . 

echo ""
echo "Browsing ngrok status page"
python -m webbrowser -t "http://localhost:4040"

while ps -p $pid > /dev/null; do
  wait $pid
done