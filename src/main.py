import requests
from src.ingestion.fetch_articles import fetch_article
from src.publishers.send_to_sqs import send_sqs
from dotenv import load_dotenv
import os
import logging

load_dotenv()
guardian_key = os.getenv("GUARDIAN_KEY")

logging.basicConfig(level=logging.INFO)


def fetch_and_send_articles(search_term, reference, date_from=None):

    try:

        filtered_articles = fetch_article(guardian_key, search_term, date_from)
        logging.info("Filtered article function has worked")

        response = send_sqs(reference, filtered_articles)

        logging.info("send_sqs function has worked")

        return response

    except Exception as e:
        logging.error(f"Error has occured - fetch_and_send_articles: {e}")

    return None
