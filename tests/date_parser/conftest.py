from typing import Callable

import pytest
from recall_me.date_parser import next_notification as n_notification


@pytest.fixture
def next_notification() -> Callable:
    return n_notification
