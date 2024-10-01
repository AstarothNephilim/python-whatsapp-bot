import pytest
from pydantic import ValidationError
from app.models import WebhookPayload, parse_webhook_payload

def test_valid_status_update(valid_status_update_payload):
    try:
        webhook = parse_webhook_payload(valid_status_update_payload)
        assert webhook.object == "whatsapp_business_account"
        assert len(webhook.entry) == 1
        entry = webhook.entry[0]
        assert entry.id == "entry_id_1"
        assert len(entry.changes) == 1
        change = entry.changes[0]
        assert change.field == "statuses"
        assert len(change.value.statuses) == 1
        status = change.value.statuses[0]
        assert status.status == "delivered"
        assert status.recipient_id == "15551234567"
        assert status.conversation.id == "conversation_id_1"
    except ValidationError as e:
        pytest.fail(f"Valid status update payload raised ValidationError: {e}")

def test_valid_text_message(valid_text_message_payload):
    try:
        webhook = parse_webhook_payload(valid_text_message_payload)
        assert webhook.object == "whatsapp_business_account"
        assert len(webhook.entry) == 1
        entry = webhook.entry[0]
        assert len(entry.changes) == 1
        change = entry.changes[0]
        assert change.field == "messages"
        assert len(change.value.messages) == 1
        message = change.value.messages[0]
        assert message.from_ == "15551234567"
        assert message.type == "text"
        assert message.text.body == "Hello, this is a test message."
    except ValidationError as e:
        pytest.fail(f"Valid text message payload raised ValidationError: {e}")

def test_valid_document_message(valid_document_message_payload):
    try:
        webhook = parse_webhook_payload(valid_document_message_payload)
        assert webhook.object == "whatsapp_business_account"
        assert len(webhook.entry) == 1
        entry = webhook.entry[0]
        assert len(entry.changes) == 1
        change = entry.changes[0]
        assert change.field == "messages"
        assert len(change.value.messages) == 1
        message = change.value.messages[0]
        assert message.from_ == "15557654321"
        assert message.type == "document"
        assert message.document.filename == "test_document.pdf"
        assert message.document.mime_type == "application/pdf"
        assert message.document.sha256 == "fake_sha256_hash_value"
    except ValidationError as e:
        pytest.fail(f"Valid document message payload raised ValidationError: {e}")

def test_invalid_message_payload(invalid_message_payload):
    result = parse_webhook_payload(invalid_message_payload)
    assert result is None, "Expected parse_webhook_payload to return None for invalid payload"
