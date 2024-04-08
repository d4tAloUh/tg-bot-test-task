import json
import typing

import pytest
from telegram import Update

from src import api
from tests.test_data.message_data import telegram_hello_message_data, queue_hello_message, telegram_hello_command_data, \
    queue_hello_command


@pytest.mark.parametrize(
    "original_message,expected_message",
    [
        pytest.param(
            telegram_hello_message_data,
            queue_hello_message,
            id="standard_message",
        ),
        pytest.param(
            telegram_hello_command_data,
            queue_hello_command,
            id="command_message",
        ),
    ],
)
def test_prepare_message_body(original_message, expected_message: dict[str, typing.Any]):
    message = api.prepare_message_for_queue(event_body=original_message)
    assert message == expected_message
    # Test that it will be parsed correctly with Update
    assert Update.de_json(expected_message, None)


@pytest.mark.parametrize(
    "original_message,expected_message",
    [
        pytest.param(
            telegram_hello_message_data,
            queue_hello_message,
            id="standard_message",
        ),
        pytest.param(
            telegram_hello_command_data,
            queue_hello_command,
            id="command_message",
        ),
    ],
)
def test_lambda_handler_success(queue_fixture, original_message, expected_message):
    response = api.lambda_handler(event={"body": original_message}, context=None)
    assert response["statusCode"] == 200
    assert response["body"] == "Success"
    # Make sure message was put in queue and was minimized
    assert queue_fixture.send_message.was_called_once()
    send_message_arg = queue_fixture.send_message.call_args.kwargs
    assert json.loads(send_message_arg["MessageBody"]) == expected_message


def test_lambda_handler_failure():
    event_data = {
        "body": {"random_body": "abc"}
    }
    response = api.lambda_handler(event={"body": event_data}, context=None)
    assert response["statusCode"] == 500
    assert response["body"] == "Failure"
