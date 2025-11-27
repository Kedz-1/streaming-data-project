import pytest
import boto3
import json
from unittest.mock import patch
from dotenv import load_dotenv
import os
from src.main import fetch_and_send_articles

load_dotenv()

@pytest.fixture
def guardian_key():

    return os.getenv('GUARDIAN_KEY')

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

@pytest.fixture
def search_term():
    return 'and'

@pytest.fixture
def example_date():
    return '2020-01-01'

@pytest.fixture
def reference():
    return 'guardian_content'


@patch('src.main.send_sqs')
@patch('src.main.fetch_article')
def test_main(mock_fetch, mock_send):
    
    mock_fetch.return_value = {'articles': 'hello'}

    mock_send.return_value = {'status':'ok'}

    result = fetch_and_send_articles('football', 'guardian_content')

    mock_fetch.assert_called_once_with(os.getenv('GUARDIAN_KEY'), 'football', None)
    mock_send.assert_called_once_with('guardian_content', {'articles': 'hello'})

    assert result == {'status': 'ok'}