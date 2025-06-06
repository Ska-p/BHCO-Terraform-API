import os
import sys
import json
import requests
import logging
import traceback

# Add the project base path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

def get_datamart_summary(datamart_id: str):
    """
    Sends a GET request to retrieve summary for a specific DataMart.

    @param datamart_id: The ID of the DataMart to query.

    Requirements:
    - `config.json` must contain:
        - `auth.BearerToken`: The authentication token.
    - Logging is configured via `utils.setup_logging()`.
    - API response is saved in `logs/response/`.

    Raises:
    - Logs and exits if `datamart_id` or `BearerToken` is missing.
    - Logs detailed information about the request, response, or errors.
    """
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    if not datamart_id:
        logging.error("❌ DataMart ID not provided as input argument.")
        print("❌ GET failed (check log)")
        return

    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ GET failed (check log)")
        return

    url = f"{credentials['base_url']}/opt/api/v1/datamartservice/datamarts/{datamart_id}/cst"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:
        logging.info(f"🔹 GET Request URL: {url}")
        response = requests.get(url, headers=headers)
        print("Response Text:", response.text)
        response.raise_for_status()

        logging.info(f"✅ GET request successfully sent for DataMart ID: {datamart_id}")
        logging.info(f"✅ Response Code: {response.status_code}")

        if not response.text.strip():
            logging.info("⚠️ Empty response received.")
            print("✅ GET successful (empty response)")
            return None

        response_data = response.json()
        formatted_json = json.dumps(response_data, indent=4)
        logging.info(f"✅ Response Body:\n{formatted_json}")

        json_path = utils.get_response_json_path("getDatamartSummary", f"datamart_{datamart_id}")
        with open(json_path, 'w') as f:
            json.dump(response_data, f, indent=4)

        print("✅ GET successful")
        return formatted_json

    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = json.dumps(response.json(), indent=4) if response.text.strip() else "No response body"
        except Exception:
            error_body = response.text
        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET failed (check log)")