## Context
Initially, I was offered a choice between 2 briefs for a freelance work. I chose a 'GDPR Obfuscation' module that sensitised personal information as I was more comfortable with the requirements - s3 end-to-end. So by necessity, in choosing the brief that I was more comfortable with meant that I wasn't as confident with the 'Streaming Data' project. Thus, I decided to complete this project in my personal time.

## Tech stack

### Python

Python was my language of choice due to its simplicity and strong ecosystem for both API integrations and cloud development.

### Requests

I used Requests to retrieve article data from The Guardian API. It provides a straightforward way to handle HTTP requests and responses while keeping the code easy to maintain.

### Boto3
Boto3 allowed me to interact directly with AWS services, particularly SQS. This made it possible to publish article data into a queue for downstream processing.

### AWS SQS
I chose SQS because it introduces a decoupled architecture. The process collecting articles does not need to know what consumes the data later, making the system more scalable and flexible.

### AWS Lambda/EventBridge
Lambda allowed the application to run without managing servers, making it cost-effective and suitable for periodic workloads. Whilst EventBridge was used to schedule automatic excecutions.

### Terraform

Terraform enabled me to provision infrastructure consistently through code. It also provided version control for infrastructure changes and simplified deployment and teardown.

### Pytest and Moto

I used Pytest for automated testing and Moto to mock AWS services. This allowed me to test functionality without creating real AWS resources or incurring cloud costs.


## Main problems
The main problems this project solved was:

    1. Retrieving Relevant Data Reliably

    The application needed to communicate with an external API, handle responses correctly, and ensure the required article information was extracted consistently.

    2. Creating a Scalable Architecture

    I wanted to avoid tightly coupling data retrieval with data processing. If requirements changed in the future, the architecture needed to remain flexible.

    3. Testing Cloud Integrations

    Testing code that interacts with AWS can be expensive and difficult if every test requires live cloud resources.

    4. Repeatable Infrastructure Deployment

    Manually creating cloud resources increases the chance of human error and is time consuming.

## Solution

    1. I built a Python service that calls The Guardian API, validates responses, and transforms article information into a structured JSON format.

    2. I introduced AWS SQS as a message broker. Articles are published as messages, allowing any future consumers to process the data independently.

    3. I implemented unit tests using Pytest and Moto. AWS services were mocked so that application behaviour could be validated without making live AWS calls.

    4. I used Terraform to create AWS resources. This made infrastructure deployment repeatable, and easy to recreate.

## Finished Product

The final solution consisted of:

    - A Python application that retrieves articles from The Guardian API.
    - Logic to transform article data into JSON messages.
    - An AWS SQS queue to receive article messages.
    - AWS Lambda to execute the workload.
    - EventBridge scheduling to automate execution.
    - Terraform-managed infrastructure.
    - Automated tests validating functionality.

## Why is this useful for companies

This project demonstrates several skills that are commonly used in production environments.

- API Integration
- Event-Driven Architecture
- Cloud Engineering
- Infrastructure as Code
- Testing and Reliability

## Future Improvements

- Improve Observability
- Expand Filtering Options
- Add Multiple Data Sources
- Containerise the Application
