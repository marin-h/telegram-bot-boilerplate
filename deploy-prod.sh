#!/bin/bash

 echo ""
echo "loading env vars"
export $(grep -v '^#' .env | xargs -0)

echo "feching data"
python3 ./src/store.py

echo "Deploying bot to GCR"
echo 
gcloud beta run deploy letras-bot --source . --set-env-vars TOKEN=${TOKEN} --allow-unauthenticated --platform managed --project $PROJECT_NAME

echo "Set Telegram webhook: curl https://api.telegram.org/bot\$TOKEN/setWebHook?url=$WEBHOOK"
curl -s "https://api.telegram.org/bot$TOKEN/setWebHook?url=$WEBHOOK" | jq .

echo "Telegram Webhook Info: curl https://api.telegram.org/bot\$TOKEN/getWebhookInfo"
echo
curl "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | jq .

