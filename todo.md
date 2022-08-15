# pre requisites
create drive folder
apis enable drive api

# prod
setup folder id envvar
google cloud run free trial https://console.cloud.google.com/freetrial/signup
SETUP gcp and token
https://nullonerror.org/2021/01/08/hosting-telegram-bots-on-google-cloud-run/
enable compute engine api (creates default service account) https://cloud.google.com/compute/docs/access/service-accounts#default_service_account

# staging
setup folder id envvar
install ngrok
setup gdrive permissions ??
for staging, create service account https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating_a_service_account and download credentials (json), set path in .env STAGING_CREDENTIALS