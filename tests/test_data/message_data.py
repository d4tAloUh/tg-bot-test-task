telegram_hello_message_data = {
    "message": {
        "channel_chat_created": False,
        "delete_chat_photo": False,
        "group_chat_created": False,
        "supergroup_chat_created": False,
        "text": "hello",
        "chat": {
            "first_name": "Test",
            "id": 111111111,
            "last_name": "Test",
            "type": "private",
            "username": "test"
        },
        "date": 1712492846,
        "message_id": 1234,
        "from": {
            "first_name": "Test",
            "id": 111111111,
            "is_bot": False,
            "is_premium": True,
            "language_code": "en",
            "last_name": "Test",
            "username": "test"
        }
    },
    "update_id": 11111111
}

telegram_hello_command_data = {"message": {"channel_chat_created": False, "delete_chat_photo": False,
             "entities": [{"length": 6, "offset": 0, "type": "bot_command"}], "group_chat_created": False,
             "supergroup_chat_created": False, "text": "/hello",
             "chat": {"first_name": "Test", "id": 111111111, "last_name": "Test", "type": "private",
                      "username": "test"}, "date": 1712492846, "message_id": 1234,
             "from": {"first_name": "Test", "id": 111111111, "is_bot": False, "is_premium": True,
                      "language_code": "en", "last_name": "Test", "username": "test"}}, "update_id": 11111111}

queue_hello_message = {
    "message": {
        "message_id": 1234,
        "chat": {
            "id": 111111111,
            "type": "private",
        },
        "text": "hello",
        "date": 1712492846,
    },
    "update_id": 11111111
}

queue_hello_command = {
    "message": {
        "message_id": 1234,
        "chat": {
            "id": 111111111,
            "type": "private",
        },
        "text": "/hello",
        "date": 1712492846,
        "entities": [{"length": 6, "offset": 0, "type": "bot_command"}]
    },
    "update_id": 11111111
}
