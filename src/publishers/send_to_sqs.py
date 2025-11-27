import boto3
import json
import logging


logging.basicConfig(level=logging.INFO)

def send_sqs(reference, articles):
    
    if not isinstance(articles, dict):
        logging.error('Invalid input, input must be a dictionary requested from fetch_article')

        raise ValueError('Expects dictionary')

    try:
        sqs = boto3.client('sqs', 'eu-west-2')        
        logging.info('Successfully connected to SQS')

        url = sqs.get_queue_url(QueueName=reference)
        queue_url = url['QueueUrl']
        logging.info(f'Queue Url: {queue_url}')

        send_message = sqs.send_message(QueueUrl = queue_url, MessageBody = json.dumps(articles))      
        logging.info(f'Successfully sent message: {send_message}')

        return send_message

    except:
        logging.error('Sending articles to message broker has been unsuccessful')
        raise ValueError('Invalid reference')
        
