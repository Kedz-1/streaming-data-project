import boto3
import json
import requests
from datetime import datetime
import logging
import os
from src.main import fetch_and_send_articles

logging.basicConfig(level=logging.INFO)

def handler(event, context):


    try:

        search_term = os.environ.get("SEARCH_TERM")
        date_from = os.environ.get("DATE_FROM", None)

        print("search_term:", search_term )
        print("date_from:", date_from)

        logging.info(f"Running Lambda with search_term='{search_term}', date_from='{date_from}'")
        
        if not search_term:
            raise ValueError("Event must include a 'search_term'")

        logging.info('Lambda function has run successfully')
        return fetch_and_send_articles(search_term, date_from)
        

    except Exception as e:

        logging.error(f'An error has occured when trying to run the lambda function: {e}')
        raise