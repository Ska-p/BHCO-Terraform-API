import os
import sys
import json
import requests
import logging
import traceback

# Add the project base path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

def post_cst_query(cst_query: str):
    """
    Sends a POST request using a CST query to retrieve DataMart data.

    @param cst_query: The CST (Capacity Scripting Tool) query to execute.

    Requirements:
    - `config.json` must contain:
        - `auth.BearerToken`: The authentication token.
    - Logging is configured via `utils.setup_logging()`.
    - API response is saved in `logs/response/`.

    Raises:
    - Logs and exits if `cst_query` or `BearerToken` is missing.
    - Logs detailed information about the request, response, or errors.
    """
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    if not cst_query:
        logging.error("❌ CST query not provided.")
        print("❌ POST failed (check log)")
        return

    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ POST failed (check log)")
        return

    url = f"{credentials['base_url']}/opt/api/v1/datamartservice/datamarts/cst"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    payload = {
        "query": cst_query,
        "options": {
            "pagenum": -1,
            "pagesize": -1
        }
    }

    try:
        payload_json = json.dumps(payload, indent=4)
        logging.info(f"🔹 POST Request URL: {url}")
        logging.info(f"🔹 POST Payload:\n{payload_json}")
    except TypeError as e:
        logging.error(f"❌ Failed to serialize JSON payload: {e}")
        print("❌ POST failed (check log)")
        return

    try:
        response = requests.post(url, headers=headers, data=payload_json)
        response.raise_for_status()

        logging.info("✅ POST request successfully sent for CST query")
        logging.info(f"✅ Response Code: {response.status_code}")

        if response.status_code == 204 or not response.text.strip():
            logging.info("⚠️ No content in response (204 No Content), skipping saving response.")
            print("✅ POST successful (no content)")
            return None

        response_data = response.json()
        formatted_json = json.dumps(response_data, indent=4)
        logging.info(f"✅ Response Body:\n{formatted_json}")

        json_path = utils.get_response_json_path("postCstQuery", "datamart_cst_result")
        with open(json_path, 'w') as f:
            json.dump(response_data, f, indent=4)

        print("✅ POST successful")
        return formatted_json

    except requests.HTTPError as http_err:
        try:
            error_body = json.dumps(response.json(), indent=4) if response.text.strip() else "No response body"
        except Exception:
            error_body = response.text
        logging.error(f"❌ API Request Error: {http_err}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")

    except requests.RequestException as e:
        logging.error(f"❌ Network/API request failed: {e}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")