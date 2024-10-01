# tests/conftest.py

import pytest
from .fixtures.payloads import (
    VALID_STATUS_UPDATE_PAYLOAD,
    VALID_TEXT_MESSAGE_PAYLOAD,
    VALID_DOCUMENT_MESSAGE_PAYLOAD,
    INVALID_MESSAGE_PAYLOAD
)

@pytest.fixture
def valid_status_update_payload():
    return VALID_STATUS_UPDATE_PAYLOAD

@pytest.fixture
def valid_text_message_payload():
    return VALID_TEXT_MESSAGE_PAYLOAD

@pytest.fixture
def valid_document_message_payload():
    return VALID_DOCUMENT_MESSAGE_PAYLOAD

@pytest.fixture
def invalid_message_payload():
    return INVALID_MESSAGE_PAYLOAD
