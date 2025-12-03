from src.publishers.send_to_sqs import send_sqs
import pytest
import boto3
from moto import mock_aws
import json


@pytest.fixture
def message():

    return {
        "response": {
            "results": [
                {
                    "webPublicationDate": "2025-11-11T17:20:20Z",
                    "webUrl": "https://www.example/url.com",
                    "webTitle": "Another one from the A-League champions!",
                },
                {
                    "webPublicationDate": "2019-11-11T17:20:20Z",
                    "webUrl": "https://www.example/2/url.com",
                    "webTitle": "Random news that shouldn't show",
                },
                {
                    "webPublicationDate": "2025-11-11T17:20:20Z",
                    "webUrl": "https://www.example/3/url.com",
                    "webTitle": "Another piece of news that possibly shou;dn't show, something about Trump I think.",
                },
                {
                    "webPublicationDate": "2010-11-11T17:20:20Z",
                    "webUrl": "https://www.example/3/url.com",
                    "webTitle": "Another piece of news that possibly shouldn't show, something about Trump again, I think, but this time with an old publication date.",
                },
            ]
        }
    }


@pytest.fixture
def reference():
    return "guardian_content"


def test_function_input_is_dict(reference):

    sqs = boto3.client("sqs", "eu-west-2")

    sqs.create_queue(QueueName=reference)
    input1 = "article: this is a mock article"

    with pytest.raises(ValueError, match="Expects dictionary"):
        send_sqs(reference, input1)


def test_function_raises_error_on_incorrect_reference(message):

    sqs = boto3.client("sqs", region_name="eu-west-2")

    with pytest.raises(ValueError, match="Invalid reference"):
        send_sqs("no-reference", message)


@mock_aws
def test_function_returns_json_body(reference, message):

    sqs = boto3.client("sqs", region_name="eu-west-2")

    queue = sqs.create_queue(QueueName=reference)
    queue_url = queue["QueueUrl"]

    send_sqs(reference, message)

    response = sqs.receive_message(QueueUrl=queue_url)

    body = json.loads(response["Messages"][0]["Body"])

    assert isinstance(body, dict)
    assert body == message


@mock_aws
def test_function_returns_message_response(reference, message):
    sqs = boto3.client("sqs", region_name="eu-west-2")

    queue = sqs.create_queue(QueueName=reference)
    queue_url = queue["QueueUrl"]

    response = send_sqs(reference, message)

    assert "MessageId" in response


@mock_aws
def test_function_returns_correctly_for_multiple_articles(reference, message):

    sqs = boto3.client("sqs", "eu-west-2")

    queue = sqs.create_queue(QueueName=reference)
    queue_url = queue["QueueUrl"]

    result = send_sqs(reference, message)

    response = sqs.receive_message(QueueUrl=queue_url)
    message = json.loads(response["Messages"][0]["Body"])

    assert len(message["response"]["results"]) == 4
    assert result["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_aws
def test_function_works_on_empty_dict(reference):
    message = {}
    sqs = boto3.client("sqs", region_name="eu-west-2")

    queue = sqs.create_queue(QueueName=reference)
    queue_url = queue["QueueUrl"]

    response = send_sqs(reference, message)

    assert "MessageId" in response
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
