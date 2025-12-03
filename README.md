# Guardian Data Ingestion streaming-data-project


## Overview

This project fetches articles from the Guardian API based on a search term and an optional date filter, then publishes the results to an Amazon SQS queue. It is designed to run both locally and as an AWS Lambda function on a scheduled basis.

## Features

- Fetches up to 10 recent articles matching a search term.

- Supports optional date_from filtering.

- Automatically sends fetched articles to an SQS queue.

- Fully deployable to AWS Lambda with environment variables.

- Logs all operations via logging and CloudWatch.


Clone the repository
## Setup
1. Clone the repository
git clone <https://github.com/Kedz-1/streaming-data-project.git> 

2. Set up the environment via make create-environment > source/venv/bin/activate

3. Download requirements via make requirements


## For local development:
Create a .env file in the root folder:

GUARDIAN_KEY= "your Guardian API key"

SEARCH_TERM= "default search term"

DATE_FROM= "optional start date YYYY-MM-DD"

QUEUE_NAME= "SQS queue name"


The code uses python-dotenv to load the API key for local testing.

## AWS Lambda

Add the following environment variables to your Lambda function:

terraform/lambda.tf

environment {
    variables = {
      SEARCH_TERM = "Default search term"
      QUEUE_NAME = aws_sqs_queue.guardian_queue.name
      DATE_FROM   = "Optional start date"
      GUARDIAN_KEY = "Your Guardian API key"
    }
  }

Queue_name is taken directly from the SQS queue defined in terraform/main.tf:
name = "Your SQS Queue name"


## Lambda invocation

The Lambda handler is handler.handler.

Trigger via EventBridge for automated scheduling (e.g., every 12 hours):

Schedule: rate(12 hours)


## Zip the contents:

cd package
zip -r ../lambda_function.zip .


Upload lambda_function.zip to AWS Lambda. (Should be completed by running terraform apply)


## Deploy Lambda

The following will deploy the lambda module. 

1. cd terraform 

2. terraform plan 

3. terraform apply

4. yes


When lambda is no longer required:

1. terraform destroy

2. yes

This will remove all lambda setup.


## Logging

Logs are written using Python’s logging module.

In Lambda, all logs are available in CloudWatch Logs.

## Notes

The project is designed to handle up to 1MB of CSV articles per run.

Future extensions may include additional file formats, more advanced filters, or retries for failed SQS sends.
