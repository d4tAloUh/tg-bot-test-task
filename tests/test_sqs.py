import json

import pytest

from unittest.mock import AsyncMock, patch, MagicMock, PropertyMock
from src import sqs
from tests.conftest import CHAT_ID
from telegram import Bot


@pytest.mark.asyncio
async def test_echo_callback(same_chat_update):
    context = AsyncMock()
    await sqs.echo_callback(update=same_chat_update, context=context)
    assert await context.bot.send_message.was_called_once()

    send_message_arg = context.bot.send_message.call_args.kwargs
    assert send_message_arg["chat_id"] == CHAT_ID
    assert send_message_arg["text"] == "Sorry, I don’t understand."


@pytest.mark.asyncio
async def test_hello_callback(same_chat_update):
    context = AsyncMock()

    await sqs.hello_callback(update=same_chat_update, context=context)
    assert await context.bot.send_message.was_called_once()

    send_message_arg = context.bot.send_message.call_args.kwargs
    assert send_message_arg["chat_id"] == CHAT_ID
    assert send_message_arg["text"] == "Hi! How can i help you?"


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(
            {
                    "message_id": 1234,
                    "chat": {
                        "id": 111111111,
                        "type": "private",
                    },
                    "text": "abcdashellogerageg",
                    "date": 1712492846,
                },
            id="hello_callback_message",
        ),
        pytest.param(
            {
                    "message_id": 1234,
                    "chat": {
                        "id": 111111111,
                        "type": "private",
                    },
                    "text": "bfsgstHeLlOregwgewr",
                    "date": 1712492846,
                },
            id="hello_callback_message_case_insensitive",
        ),
        pytest.param(
            {
                "message_id": 1234,
                "chat": {
                    "id": 111111111,
                    "type": "private",
                },
                "text": "/hello",
                "date": 1712492846,
                "entities": [{"length": 6, "offset": 0, "type": "bot_command"}]
            },
            id="hello_callback_command",
        ),
    ],
)
@pytest.mark.asyncio
@patch("src.sqs.hello_callback")
async def test_main_process_update_hello(hello_callback_mock, message, monkeypatch):
    context = AsyncMock()
    event = {
        "Records": [
            {
                "body": json.dumps({
                    "message": message,
                    "update_id": 11111111
                })
            }
        ]
    }
    await sqs.main(event=event, context=context)
    assert await hello_callback_mock.was_called_once()
    assert hello_callback_mock.call_count == 1


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(
            {
                "message_id": 1234,
                "chat": {
                    "id": 111111111,
                    "type": "private",
                },
                "text": "abcd  ah ello",
                "date": 1712492846,
            },
            id="echo_callback_message",
        ),
    ],
)
@pytest.mark.asyncio
@patch("src.sqs.echo_callback")
async def test_main_process_update_echo(echo_callback_mock, message, monkeypatch):
    context = AsyncMock()
    event = {
        "Records": [
            {
                "body": json.dumps({
                    "message": message,
                    "update_id": 11111111
                })
            }
        ]
    }
    await sqs.main(event=event, context=context)
    assert await echo_callback_mock.was_called_once()
    assert echo_callback_mock.call_count == 1
