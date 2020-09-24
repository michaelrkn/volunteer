# volunteer

Deployed on Heroku

`migrations` folder must be included in all code changes; do not `.gitignore` this folder. Before pushing, run `makemigrations` and `migrate` locally, then once deployed, `heroku run` both commands. No need to do `collectstatic`.

The data for registrations is gathered from the Civis API (through the custom management command `refreshCivis`). The Civis API only allows for creation of API keys that last 30 days, so the `CIVIS_API_KEY` Heroku config var must be updated at least every 30 days

## Environmental Variables

Before you can start the app, you'll need to set these environmental variables:

* SECRET_KEY
* EMAIL_HOST_PASSWORD
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME
* AWS_S3_REGION_NAME
* AWS_S3_CUSTOM_DOMAIN
* SENDGRID_API_KEY
