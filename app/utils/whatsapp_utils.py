import logging
from flask import Blueprint, request, jsonify, current_app
import json
import requests
from typing import Optional

# from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )





def generate_response(response):
    # Return text in uppercase
    return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response

def get_media_url(media_id: str) -> Optional[str]:
    """
    Retrieves the media URL from WhatsApp Business API using the provided media ID.

    Args:
        media_id (str): The ID of the media to retrieve.

    Returns:
        Optional[str]: The URL of the media if successful, else None.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{media_id}/"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.Timeout:
        logging.error(f"Timeout occurred while fetching media URL for media_id: {media_id}")
        return None
    except requests.ConnectionError:
        logging.error(f"Connection error occurred while fetching media URL for media_id: {media_id}")
        return None
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching media URL for media_id {media_id}: {http_err}")
        return None
    except requests.RequestException as req_err:
        logging.error(f"Request exception occurred while fetching media URL for media_id {media_id}: {req_err}")
        return None

    try:
        body = response.json()
    except ValueError:
        logging.error(f"Invalid JSON response while fetching media URL for media_id: {media_id}")
        return None

    media_url = body.get("url")
    if not media_url:
        logging.error(f"'url' not found in the response body for media_id: {media_id}")
        return None

    return media_url



def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def get_message_type(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    msg_type = message["type"]

    return msg_type


def process_text_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def process_document_whatsapp_message(body):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }


    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    media_id = message["document"]["id"]
    media_filename = message["document"]["filename"]

    media_url = get_media_url(media_id)
    logging.info(f'This is the MEDIA URL {media_url}')

    # Make the GET request
    response = requests.get(media_url, headers=headers)
    output_file = media_filename
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the file
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Media downloaded successfully and saved to '{output_file}'.")
    else:
        print(f"Failed to download media. Status code: {response.status_code}")
        print(f"Response message: {response.text}")

        return media_url




def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
