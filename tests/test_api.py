import json

from src import api
from tests.test_data.message_data import telegram_message_data, queue_message


def test_prepare_message_body():
    message = api.prepare_message_for_queue(event_body=telegram_message_data)
    assert message == queue_message


def test_lambda_handler_success(queue_fixture):
    response = api.lambda_handler(event={"body":telegram_message_data}, context=None)
    assert response["statusCode"] == 200
    assert response["body"] == "Success"
    # Make sure message was put in queue and was minimized
    assert queue_fixture.send_message.was_called_once()
    send_message_arg = queue_fixture.send_message.call_args.kwargs
    assert json.loads(send_message_arg["MessageBody"]) == queue_message


def test_lambda_handler_failure():
    event_data = {
        "body": {"random_body": "abc"}
    }
    response = api.lambda_handler(event={"body":event_data}, context=None)
    assert response["statusCode"] == 500
    assert response["body"] == "Failure"
