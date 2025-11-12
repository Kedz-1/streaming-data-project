import requests
from dotenv import load_dotenv
import os 
import re
from datetime import datetime

load_dotenv()

guardian_key = os.getenv('GUARDIAN_KEY')


def fetch_article(guardian_key, search_term, reference='articles', date_from=None):


    url = f'https://content.guardianapis.com/search?api-key={guardian_key}'

    pattern = rf'\b{re.escape(search_term)}\b'

    try: 
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        articles = data['response']['results']

        if date_from:
            input_date = datetime.strptime(date_from, '%Y-%m-%d')
        
        else:
            input_date = None

        articles_list = [
                {
                'webPublicationDate': article.get('webPublicationDate', ''),
                'webTitle': article.get('webTitle', ''),
                'webUrl': article.get('webUrl', '')
                } 
                for article in articles 
                if re.search(pattern, article['webTitle'], re.IGNORECASE) 
                and (not input_date or input_date <= datetime.strptime(article['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ'))
            ]

       
        

        if not articles_list:
            return {
                'statusCode': response.status_code,
                reference: [],
                'message': 'No articles found matching your search terms'
            }

        ten_articles = articles_list[0:10]

        return {
            'statusCode': response.status_code,
            reference: ten_articles
        }

    except requests.exceptions.HTTPError:

        try:

            error = response.json()            
            message = error.get('message', 'HTTP Error' )
 
        except Exception:
            message = 'HTTP Error'

        return {
            'statusCode' : response.status_code,
            'message' : message
        }

    except requests.exceptions.RequestException as e:

        return{
            'statusCode' : 500,
            'message' : str(e)
        }

print(fetch_article(guardian_key, 'trump', 'guardian_content', '2024-11-20'))



'''
The tool will publish data to the message broker in the following JSON
format:
{
"webPublicationDate": "2023-11-21T11:11:31Z",
"webTitle": "Who said what: using machine learning to correctly attribute
quotes",
"webUrl": "https://www.theguardian.com/info/2023/nov/21/who-saidwhat-using-machine-learning-to-correctly-attribute-quotes"
}
These fields are the minimum required. Others may be added at your
discretion.
'''




# web_title = articles['response']['results'][0]['webTitle']
        # web_url = articles['response']['results'][0]['webUrl']
        # web_publication_date = articles['response']['results'][0]['webPublicationDate']
        
        # return {
        #     'statusCode' : response.status_code,
        #     'webPublicationDate': web_publication_date,
        #     'webTitle': web_title,
        #     'webUrl': web_url
        
        # }