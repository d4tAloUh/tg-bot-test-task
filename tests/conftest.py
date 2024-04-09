from unittest.mock import patch, MagicMock, PropertyMock, AsyncMock

import pytest
from telegram import User, Bot

CHAT_ID = "123456"


@pytest.fixture(scope="session", autouse=True)
def queue_fixture():
    with patch("src.api.queue") as queue:
        yield queue


@pytest.fixture()
def same_chat_update():
    update = MagicMock()
    update.effective_chat.id = CHAT_ID
    return update


@pytest.fixture()
def bot_user():
    return User.de_json({
            "can_join_groups": False,
            "can_read_all_group_messages": False,
            "first_name": "test_bot",
            "id": 1234567890,
            "is_bot": True,
            "supports_inline_queries": True,
            "username": "test_bot",
            "can_connect_to_business": False
        },
        bot=None
    )


@pytest.fixture(scope='function', autouse=True)
def mock_bot_user(bot_user):
    with patch.object(Bot, "_bot_user", new_callable=PropertyMock) as property_mock:
        property_mock.return_value = bot_user
        yield property_mock


@pytest.fixture(scope='function', autouse=True)
def mock_bot_get_me(monkeypatch):
    monkeypatch.setattr(Bot, "get_me", AsyncMock())
