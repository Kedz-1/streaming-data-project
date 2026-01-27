import requests
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

guardian_key = os.getenv("GUARDIAN_KEY")


def fetch_article(guardian_key, search_term, date_from=None):

    '''
    Fetch articles from the Guardian Content API and filter them by a search
    term and an optional publication date. 
    
    Args:
        guardian_key (url)- A url providing access to the the guardian API.      

        search_term (str) - Searches through the article body, filtering by a search term.

        date_from (str) - Searches through the article, filtering by a chosen date ('yyyy-mm-dd' format). Defaults to None.
    
    Returns:

        dict:
                On success:
                    {
                        "statusCode": int,
                        "articles": list[dict]
                    }

                Each article dictionary contains:
                    - webPublicationDate (str)
                    - webTitle (str)
                    - webUrl (str)

                If no matching articles are found:
                    {
                        "statusCode": int,
                        "articles": [],
                        "message": str
                    }

                On error:
                    {
                        "statusCode": int,
                        "message": str
                    }

        Raises:
            None explicitly. All HTTP and request-related errors are caught
            and returned as part of the response dictionary.

    '''

    url = f"https://content.guardianapis.com/search?api-key={guardian_key}"


    # Compile a whole-word, case-insensitive regex pattern for title matching
    # re.escape ensures special characters in the search term are treated literally
    pattern = rf"\b{re.escape(search_term)}\b"

    try:
        # Make request to Guardian API
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()
        articles = data["response"]["results"]

        # Convert date_from to datetime object if provided
        if date_from:
            input_date = datetime.strptime(date_from, "%Y-%m-%d")

        else:
            input_date = None

        # Filter and transform article, filling relevant fields. 
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

        # Handle case where no articles found
        if not articles_list:
            return {
                "statusCode": response.status_code,
                "articles": [],
                "message": "No articles found matching your search terms",
            }

        # Limit result to 10 articles
        ten_articles = articles_list[0:10]

        return {"statusCode": response.status_code, "articles": ten_articles}

    except requests.exceptions.HTTPError:

        # Attempt to raise error message
        try:

            error = response.json()
            message = error.get("message", "HTTP Error")

        except Exception:
            message = "HTTP Error"

        return {"statusCode": response.status_code, "message": message}

    # Catch all for network, connection and timeout errors
    except requests.exceptions.RequestException as e:

        return {"statusCode": 500, "message": str(e)}
