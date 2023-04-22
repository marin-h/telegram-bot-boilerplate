#!/bin/bash

 echo ""
echo "loading env vars"
export $(grep -v '^#' .secrets | xargs -0)

echo "Deploying bot to GCR"
echo 
gcloud beta run deploy mate-bot --source . --set-env-vars "TOKEN=${TOKEN},ADMIN_USERS=${ADMIN_USERS},CONFIG_FOLDER_ID=${PROD_CONFIG_FOLDER_ID},APP_CONFIG_PATH=${APP_CONFIG_PATH}" --allow-unauthenticated --platform managed --project $PROJECT_ID    

WEBHOOK=$(gcloud run services describe mate-bot --project $PROJECT_ID --region us-central1 --format 'value(status.url)')

echo "Set Telegram webhook: curl https://api.telegram.org/bot$TOKEN/setWebHook?url=$WEBHOOK"
curl -s "https://api.telegram.org/bot$TOKEN/setWebHook?url=$WEBHOOK" | jq .

echo "Telegram Webhook Info"
echo
curl "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | jq .

