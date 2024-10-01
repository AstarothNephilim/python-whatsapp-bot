from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal, Union, Annotated
import json
import logging


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

# Change Models
class ChangeMessages(BaseModel):
    field: Literal['messages']
    value: ValueMessages

class ChangeStatuses(BaseModel):
    field: Literal['messages']  # 'field' remains 'messages' for statuses as per payload
    value: ValueStatuses

# Union of Change Types Without Discriminator
Change = Union[ChangeMessages, ChangeStatuses]



# ---------------------------
# Webhook Models
# ---------------------------


class Entry(BaseModel):
    id: str
    changes: List[Change]

class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]

    def get_changes(self) -> Change:
        changes = self.entry[0].changes[0]
        return changes
    
    def get_type_of_webhook(self) -> str:
        change = self.get_changes()

        if isinstance(change,ChangeStatuses):
            return 'status'
        elif isinstance(change,ChangeMessages):
            return 'message'
        else:
            return 'unknown'

    def is_message(self):
        change = self.get_changes()
        return isinstance(change,ChangeMessages)
    
    def is_status(self):
        change = self.get_changes()
        return isinstance(change,ChangeStatuses)
    
    def is_text_message(self):
        change = self.get_changes()

        if not isinstance(change,ChangeMessages):
            return logging.error("Not a message")
        
        message = change.value.messages[0]
        return isinstance(message, TextMessage)

    def is_document_message(self):
        change = self.get_changes()

        if not isinstance(change,ChangeMessages):
            return logging.error("Not a message")
        
        message = change.value.messages[0]
        return isinstance(message, DocumentMessage)


    def get_body_of_text_message(self):
        if self.is_text_message():
            change = self.get_changes()
            message = change.value.messages[0]
            body = message.text.body
            return body
        else:
            return "Not a message"


    def get_document_of_document_message(self):
        if self.is_document_message():
            change = self.get_changes()
            message = change.value.messages[0]
            document = message.document

        return document


        

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
    
    

