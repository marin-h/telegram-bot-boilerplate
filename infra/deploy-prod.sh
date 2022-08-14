#!/bin/bash

 echo ""
echo "loading env vars"
export $(grep -v '^#' .secrets | xargs -0)

echo "Deploying bot to GCR"
echo 
gcloud beta run deploy mate-bot --source . --set-env-vars TOKEN=${TOKEN} --set-env-vars CONFIG_FOLDER_ID=${PROD_CONFIG_FOLDER_ID} --set-env-vars APP_CONFIG_PATH=${APP_CONFIG_PATH} --allow-unauthenticated --platform managed --project $PROJECT_ID    

# WEBHOOK=https://mate-bot-f4tgy3ogpa-uc.a.run.app

# echo "Set Telegram webhook: curl https://api.telegram.org/bot$TOKEN/setWebHook?url=$WEBHOOK"
# curl -s "https://api.telegram.org/bot$TOKEN/setWebHook?url=$WEBHOOK" | jq .

echo "Telegram Webhook Info"
echo
curl "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | jq .

