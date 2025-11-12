from src.fetch_articles import fetch_article
import pytest
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import re


load_dotenv()

@pytest.fixture
def guardian_key():

    return os.getenv('GUARDIAN_KEY')

@pytest.fixture
def example_search_term():
    return 'Trump'

@pytest.fixture
def example_reference():
    return 'guardian_content'

@pytest.fixture
def example_date():
    return '2020-01-01'

@pytest.fixture
def mock_guardian_response():

    return {
                'response':{
                    'results':[
                    {
                        'webPublicationDate': '2025-11-11T17:20:20Z',
                        'webUrl': 'https://www.example/url.com',
                        'webTitle': 'Another one from the A-League champions!'
                    },
                    {
                        'webPublicationDate': '2019-11-11T17:20:20Z',
                        'webUrl': 'https://www.example/2/url.com',
                        'webTitle': 'Random news that shouldn\'t show'
                    },
                    {
                        'webPublicationDate': '2025-11-11T17:20:20Z',
                        'webUrl': 'https://www.example/3/url.com',
                        'webTitle': 'Another piece of news that possibly shou;dn\'t show, something about Trump I think.'
                    },
                    {
                        'webPublicationDate': '2010-11-11T17:20:20Z',
                        'webUrl': 'https://www.example/3/url.com',
                        'webTitle': 'Another piece of news that possibly shouldn\'t show, something about Trump again, I think, but this time with an old publication date.'
                    }
                ]
            }
        }


def test_reference_is_present_in_result(guardian_key, example_search_term, example_reference):

    result = fetch_article(guardian_key, example_search_term, example_reference)

    assert example_reference in result.keys()


def test_returns_json_format(guardian_key, example_search_term):

    result = fetch_article(guardian_key, example_search_term)

    assert isinstance(result, dict)


def test_raises_200_on_correct_key(guardian_key, example_search_term):
   
    result = fetch_article(guardian_key, example_search_term)

    assert result['statusCode'] == 200
    


def test_raises_401_on_incorrect_key(guardian_key, example_search_term):
    
    result = fetch_article(guardian_key + '11', example_search_term)
    
    assert result['statusCode'] == 401
    assert result['message'] == 'Unauthorized'


def test_handles_network_error(monkeypatch, guardian_key, example_search_term):

    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("No network")

    
    monkeypatch.setattr('requests.get', mock_get)

    result = fetch_article(guardian_key, example_search_term)

    assert result['statusCode'] == 500
    assert result['message'] == 'No network'


def test_function_returns_message_when_no_articles(monkeypatch, guardian_key, example_search_term, example_reference):


    class MockResponse:
        
        status_code = 200

        def raise_for_status(self):
            pass
        
        def json(self):
            return {'response': {'results': []} }


    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)

    result = fetch_article(guardian_key, example_search_term, example_reference)


    print(result)
    assert result['statusCode'] == 200
    assert len(result[example_reference]) == 0
    assert isinstance(result[example_reference], list)
    assert result['message'] == 'No articles found matching your search terms'
   


def test_reference_defaults_to_article_when_no_input(guardian_key, example_search_term):

    result = fetch_article(guardian_key, example_search_term)

    assert 'articles' in result.keys()


def test_function_returns_up_to_10_articles_when_search_term_present(guardian_key, example_search_term, example_reference, mock_guardian_response, monkeypatch):

    class MockResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return mock_guardian_response

    
    def mock_get(*args, **kwargs):
        return MockResponse()

    
    monkeypatch.setattr('requests.get', mock_get)
            

    result = fetch_article(guardian_key, example_search_term, example_reference)

    print(result)

    assert 1<= len(result[example_reference]) <=10

    for article in result[example_reference]:
        assert 'webPublicationDate' in article
        assert 'webTitle' in article
        assert 'webUrl' in article



def test_function_returns_articles_containing_search_term(guardian_key, example_search_term, mock_guardian_response, monkeypatch):

    class MockResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return mock_guardian_response

    
    def mock_get(*args, **kwargs):
        return MockResponse()

    
    monkeypatch.setattr('requests.get', mock_get)

    pattern = rf'\b{re.escape(example_search_term)}\b'

    result = fetch_article(guardian_key, example_search_term)

    
    assert all(re.search(pattern, x['webTitle'], re.IGNORECASE) for x in result['articles'])


def test_function_does_not_crash_regex_on_special_character(guardian_key, mock_guardian_response, monkeypatch):


    example_search_term = 'A-League'

    pattern = rf'\b{re.escape(example_search_term)}\b'

    class MockResponse:
        
        status_code = 200

        def raise_for_status(self):
            pass
        
        def json(self):
            return mock_guardian_response


    def mock_get(*args, **kwargs):
        return MockResponse()

    
    monkeypatch.setattr('requests.get', mock_get)

    result = fetch_article(guardian_key, example_search_term)


    assert all(re.search(pattern, x['webTitle'], re.IGNORECASE) for x in result['articles'])
    assert len(result['articles']) == 1



def test_function_returns_articles_from_a_particular_date(guardian_key, example_search_term, example_date, mock_guardian_response, monkeypatch):

    class MockResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return mock_guardian_response

    
    def mock_get(*args, **kwargs):
        return MockResponse()

    
    monkeypatch.setattr('requests.get', mock_get)

    result = fetch_article(guardian_key, example_search_term, date_from=example_date)

    result_date = datetime.strptime(example_date, '%Y-%m-%d')
    web_date = [datetime.strptime(x['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ').date() for x in result['articles']]


    assert all(x >= result_date.date() for x in web_date)
    assert len(result['articles']) == 1


def test_function_returns_no_articles_when_not_in_date(guardian_key, example_search_term, mock_guardian_response, monkeypatch):

    example_date = '2050-01-01'
    
    class MockResponse:
        
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return mock_guardian_response

    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr('requests.get', mock_get)

    
    result = fetch_article(guardian_key, example_search_term, date_from=example_date)

    result_date = datetime.strptime(example_date, '%Y-%m-%d')

    assert len(result['articles']) == 0


