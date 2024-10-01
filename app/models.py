from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal, Union, Annotated
import json

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

# Status models
class StatusConversationOrigin(BaseModel):
    type: str

class StatusConversation(BaseModel):
    id: str
    origin: StatusConversationOrigin

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str

class Status(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: StatusConversation
    pricing: Pricing

class ValueStatuses(BaseModel):
    messaging_product: str
    metadata: Metadata
    statuses: List[Status]

'''
Message Models
'''
class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

'''
Different types of message
'''
class TextMessageContent(BaseModel):
    body: str

class DocumentMessageContent(BaseModel):
    filename: str
    mime_type: str
    sha256: str
    id: str

class MessageBase(BaseModel):
    from_: str = Field(..., alias='from')
    id: str
    timestamp: str

    model_config = dict(populate_by_name=True)

class TextMessage(MessageBase):
    type: Literal['text']
    text: TextMessageContent

class DocumentMessage(MessageBase):
    type: Literal['document']
    document: DocumentMessageContent

# Use discriminated union based on the 'type' field
Message = Annotated[Union[TextMessage, DocumentMessage], Field(discriminator='type')]

# Messages Value
class ValueMessages(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[Contact]
    messages: List[Message]

class ChangeMessages(BaseModel):
    field: Literal['messages']
    value: ValueMessages

class ChangeStatuses(BaseModel):
    field: Literal['statuses']
    value: ValueStatuses

# Use discriminated union for Change based on the 'field' value
Change = Annotated[Union[ChangeMessages, ChangeStatuses], Field(discriminator='field')]

# Entry and root Models
class Entry(BaseModel):
    id: str
    changes: List[Change]

class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]



def parse_webhook_payload(payload: str):
    """
    Parses the JSON webhook payload into a WebhookPayload object.

    Args:
        payload (str): The JSON string payload received from the webhook.

    Returns:
        Optional[WebhookPayload]: The parsed payload object if successful, else None.
    """
    try:
        payload_dict = json.loads(payload)
        webhook_payload = WebhookPayload(**payload_dict)
        return webhook_payload
    
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())
        return None
    
    

