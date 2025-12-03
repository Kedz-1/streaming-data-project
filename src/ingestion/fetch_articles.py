import requests
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

guardian_key = os.getenv("GUARDIAN_KEY")


def fetch_article(guardian_key, search_term, date_from=None):

    url = f"https://content.guardianapis.com/search?api-key={guardian_key}"

    pattern = rf"\b{re.escape(search_term)}\b"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        articles = data["response"]["results"]

        if date_from:
            input_date = datetime.strptime(date_from, "%Y-%m-%d")

        else:
            input_date = None

        articles_list = [
            {
                "webPublicationDate": article.get("webPublicationDate", ""),
                "webTitle": article.get("webTitle", ""),
                "webUrl": article.get("webUrl", ""),
            }
            for article in articles
            if re.search(pattern, article["webTitle"], re.IGNORECASE)
            and (
                not input_date
                or input_date
                <= datetime.strptime(
                    article["webPublicationDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
            )
        ]

        if not articles_list:
            return {
                "statusCode": response.status_code,
                "articles": [],
                "message": "No articles found matching your search terms",
            }

        ten_articles = articles_list[0:10]

        return {"statusCode": response.status_code, "articles": ten_articles}

    except requests.exceptions.HTTPError:

        try:

            error = response.json()
            message = error.get("message", "HTTP Error")

        except Exception:
            message = "HTTP Error"

        return {"statusCode": response.status_code, "message": message}

    except requests.exceptions.RequestException as e:

        return {"statusCode": 500, "message": str(e)}


print(fetch_article(guardian_key, "and", "2024-11-20"))
