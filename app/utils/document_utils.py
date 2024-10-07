import logging
from flask import Blueprint, request, jsonify, current_app
import requests
from typing import Optional
from pathlib import Path
from .adr_processor import preprocess_adr_data

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


def download_document_from_webhook(webhook):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    document = webhook.get_document_of_document_message()
    logging.info(f'Document message {document.filename} received. Will attempt to extract media_url')
    media_url = get_media_url(document.id)
    logging.info(f'Media URL: {media_url}')

    # Make the GET request
    response = requests.get(media_url, headers=headers)
    output_file = document.filename

    # Define the path to save the file (e.g., app/data/)
    flask_path = Path(current_app.root_path) / 'data'
    flask_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Complete file path
    output_path = flask_path / output_file
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the file
        with open(output_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Media downloaded successfully and saved to '{output_path}'.")
        return output_path
    else:
        logging.error(f"Failed to download media. Status code: {response.status_code}")
        print(f"Response message: {response.text}")

        return None


def process_document_webhook(webhook):
    document_path = download_document_from_webhook(webhook)
    
    if 'adr' in document_path.name:
        adr_dataframe = preprocess_adr_data(document_path)
        print(adr_dataframe.head())

    else:
        print("This is not a valid adrcsv!")
    
