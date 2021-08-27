# Create Telegram Bot app

Boilerplate scripts and Dockerfile to:

* Deploy on Google Cloud Run - using free tier
* Amazingly easy to deploy staging environment, locally with ngrok

### Requirements

* docker
* python 3.7
* pip
* google-cloud-sdk
* ngrok (optional, for staging only)


### Configuration

##### Telegram BOT authentication

Add this vars to a .env file:

```
TELEGRAM_USERNAME="username"
TOKEN=token_prod
TEST_TOKEN=token_staging
```

Deploy configuration

```
# production
PROJECT_NAME=my-gcr-project 

# staging 
CONTAINER_NAME=my-telegram-bot
LOG_DIR=logs
PORT=8888
```

### Deploy

##### Production environment

Deploy on Google Cloud Run (runs on free tier)

```bash
$ ./infra/deploy-prod.sh
```

##### Staging environment


Run local container and connect it to a telegram bot.

```bash

./infra/deploy-staging.sh
```