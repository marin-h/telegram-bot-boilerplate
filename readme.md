# Telegram Bot App Boilerplate

Boilerplate scripts, Dockerfile, and API to:

* Deploy on Google Cloud Run - using free tier
* Amazingly easy to deploy staging environment, locally with ngrok

### Requirements

* google-cloud-sdk

For staging env:

* docker
* python 3.7
* pip
* ngrok


### Configuration

#### .env file:

##### Telegram BOT authentication

```
TELEGRAM_USERNAME="username"
TOKEN=token_prod
TEST_TOKEN=token_staging
```

##### Deploy configuration

Production

```
PROJECT_NAME=my-gcr-project 
```

Staging

``` 
CONTAINER_NAME=my-telegram-bot
LOG_DIR=logs
PORT=8888
```

### Deploy

##### Production environment

Deploy on Google Cloud Run (runs on free tier)

```bash
./deploy-prod.sh
```

##### Staging environment


Run local container and connect it to a telegram bot.

```bash

./deploy-staging.sh
```
