from unittest.mock import patch

import pytest


@pytest.fixture(scope="session", autouse=True)
def queue_fixture():
    with patch("src.api.queue") as queue:
        yield queue
