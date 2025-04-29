import os
import sys
import json
import requests
import logging
import traceback

# Add the project base path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

def post_datamart_data(datamart_id: str = None):
    """
    Sends a POST request to retrieve data from a specific DataMart.

    @param datamart_id: The ID of the DataMart to query. If not provided, it will attempt to retrieve it from `config.json`.

    Requirements:
    - `config.json` must contain:
        - `auth.BearerToken`: The authentication token.
        - Optionally `datamart.datamart_id` if not provided manually.
    - Logging is configured via `utils.setup_logging()`.
    - API response is saved in `logs/response/`.

    Raises:
    - Logs and exits if `datamart_id` or `BearerToken` is missing.
    - Logs detailed information about the request, response, or errors.
    """

    # Load configuration and setup logging
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    # Retrieve datamart_id if not passed
    if datamart_id is None:
        datamart_id = config.get("datamart", {}).get("datamart_id", None)
        if datamart_id is None:
            logging.error("❌ DataMart ID not found! Provide it as a parameter or add it to `config.json`.")
            print("❌ POST failed (check log)")
            return

    # Retrieve token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ POST failed (check log)")
        return
    
    # Build URL and headers
    
    url = f"{credentials["base_url"]}/opt/api/v1/datamartservice/datamarts/{datamart_id}/data"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Payload
    payload = {
        "options": {
            "pagenum": 0,
            "pagesize": -1
        }
    }

    try:
        payload_json = json.dumps(payload, indent=4)
        logging.info(f"🔹 POST Request URL: {url}")
        #logging.info(f"🔹 POST Payload:\n{payload_json}")
    except TypeError as e:
        logging.error(f"❌ Failed to serialize JSON payload: {e}")
        print("❌ POST failed (check log)")
        return

    try:
        response = requests.post(url, headers=headers, data=payload_json)
        response.raise_for_status()

        logging.info(f"✅ POST request successfully sent for DataMart ID: {datamart_id}")
        logging.info(f"✅ Response Code: {response.status_code}")

        if response.status_code == 204 or not response.text.strip():
            logging.info("⚠️ No content in response (204 No Content), skipping saving response.")
            print("✅ POST successful")
            return None

        # Process and save JSON response
        try:
            response_data = response.json()
            formatted_json = json.dumps(response_data, indent=4)
            logging.info(f"✅ Response Body:\n{formatted_json}")

            json_path = utils.get_response_json_path("postDatamartData", f"datamart_{datamart_id}")
            with open(json_path, 'w') as f:
                json.dump(response_data, f, indent=4)

            print("✅ POST successful")
            return formatted_json

        except json.JSONDecodeError:
            logging.warning("⚠️ Response was not valid JSON, skipping saving response.")

    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = json.dumps(response.json(), indent=4) if response.text.strip() else "No response body"
        except Exception:
            error_body = response.text
        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")
