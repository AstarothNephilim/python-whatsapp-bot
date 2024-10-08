import logging
import json
from pydantic import ValidationError
from flask import Blueprint, request, jsonify, current_app
from .utils.whatsapp_security import verify
from .decorators.security import signature_required
from .utils.document_utils import process_document_webhook
webhook_blueprint = Blueprint("webhook", __name__)

from app.models.payload_models import *



def process_raw_payload(request):
    body = request.get_json()
    json_str_body = json.dumps(body)

    webhook = parse_webhook_payload(json_str_body)
    logging.info(f'Webhook received: {webhook}')
    return webhook


def status_webhook_handler(webhook):
    phone,status = webhook.get_phone_status()
    print(f'This is the status: {phone},{status}')

    return phone,status


def text_webhook_handler(webhook):
    body = webhook.get_body_of_text_message()
    print(f'This is the body of the message:  {body}')
    return body



def dynamic_webhook_handler(webhook):

    function_type_dict = {'status':status_webhook_handler,'text':text_webhook_handler,'document':process_document_webhook}
    webhook_type = webhook.get_type_of_webhook()

    #Check that we are dealing with managed webhooks
    if webhook_type not in function_type_dict.keys():
        raise Exception("This payload model has not been defined yet")

    webhook_func = function_type_dict[webhook_type]

    return webhook_func(webhook)

def new_handle_message():
    try:
        processed_payload = process_raw_payload(request)
        result = dynamic_webhook_handler(processed_payload)
        print(result)
        return jsonify({'status':'ok'}),200

    except ValidationError as e:
        logging.error(f"Validation failed! \n {e.json()}")
        return (
                    jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                    404,
                )
    
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400
    
    except Exception as e:
        logging.error("Unexpected exception")
        return jsonify({"status": "error", "message": "ERROR"}), 400


@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return verify()

@webhook_blueprint.route("/webhook", methods=["POST"])
@signature_required
def webhook_post():
    return new_handle_message()


