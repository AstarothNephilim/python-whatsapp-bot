# tests/fixtures/payloads.py

import json

# Valid Status Update Payload
VALID_STATUS_UPDATE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_1",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "statuses": [
                            {
                                "id": "status_id_1",
                                "status": "delivered",
                                "timestamp": "1627773291",
                                "recipient_id": "15551234567",
                                "conversation": {
                                    "id": "conversation_id_1",
                                    "origin": {
                                        "type": "service"
                                    }
                                },
                                "pricing": {
                                    "billable": True,
                                    "pricing_model": "CBP",
                                    "category": "service"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
})

# Valid Text Message Payload
VALID_TEXT_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_2",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Alice"
                                },
                                "wa_id": "15551234567"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15551234567",
                                "id": "message_id_1",
                                "timestamp": "1627771715",
                                "text": {
                                    "body": "Hello, this is a test message."
                                },
                                "type": "text"
                            }
                        ]
                    }
                }
            ]
        }
    ]
})

# Valid Document Message Payload
VALID_DOCUMENT_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_3",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Bob"
                                },
                                "wa_id": "15557654321"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15557654321",
                                "id": "message_id_2",
                                "timestamp": "1627773047",
                                "type": "document",
                                "document": {
                                    "filename": "test_document.pdf",
                                    "mime_type": "application/pdf",
                                    "sha256": "fake_sha256_hash_value",
                                    "id": "document_id_1"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
})

# Invalid Payload Example: Missing 'type' field in message
INVALID_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_4",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Charlie"
                                },
                                "wa_id": "15559876543"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15559876543",
                                "id": "message_id_3",
                                "timestamp": "1627771715",
                                "text": {
                                    "body": "This message lacks a type field."
                                }
                                # 'type' field is missing here
                            }
                        ]
                    }
                }
            ]
        }
    ]
})
