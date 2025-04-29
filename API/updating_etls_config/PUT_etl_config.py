import requests
import json
import utils
import logging
import traceback

def put_etl_configuration(erid: str = None, modified_body: dict = None):
    """
    Updates the configuration of a specific ETL process using a PUT request.

    @param erid: The ETL process ID. If not provided, it will be retrieved from `config.json`.
    @param modified_body: A dictionary containing the ETL configuration. If not provided, it will be retrieved from `config.json`.
    """

    # Load Configuration & Setup Logging
    config = utils.load_config()
    utils.setup_logging()
    credentials = utils.load_credentials()

    # Retrieve ERID
    if erid is None:
        erid = config.get("etl", {}).get("erid", None)
        if erid is None:
            logging.error("❌ ERID not found! Provide it as a parameter or add it to `config.json`.")
            print("❌ PUT failed (check log)")
            return

    # Retrieve Bearer Token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ PUT failed (check log)")
        return

    # Retrieve modified_body
    if modified_body is None:
        modified_body = config.get("etl", {}).get("modifiedBody", None)
        if modified_body is None:
            logging.error("❌ No `modifiedBody` found in config.json.")
            print("❌ PUT failed (check log)")
            return

    # Ensure `modified_body` is a dictionary
    if isinstance(modified_body, str):
        try:
            modified_body = json.loads(modified_body)
        except json.JSONDecodeError:
            logging.error("❌ `modifiedBody` must be a valid JSON object.")
            print("❌ PUT failed (check log)")
            return

    # Ensure encryption passphrase is added
    modified_body['encryption_passphrase'] = config.get("auth", {}).get("encryption_passphrase", None)
    
    url = f"{credentials['base_url']}/opt/api/v1/backend/etls/{erid}/configuration"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:
        payload = json.dumps(modified_body, indent=4)
        logging.info(f"🔹 PUT Request URL: {url}")
        logging.info(f"🔹 PUT Payload:\n{payload}")
    except TypeError as e:
        logging.error(f"❌ Failed to serialize JSON: {e}")
        print("❌ PUT failed (check log)")
        return

    try:
        response = requests.put(url, headers=headers, data=payload)
        response.raise_for_status()

        # Log full response
        logging.info(f"✅ PUT ETL configuration updated successfully for ERID: {erid}")
        logging.info(f"✅ Response Code: {response.status_code}")
        logging.info(f"✅ Response Body:\n{response.text}")

        # Save JSON response only if present (e.g. status != 204)
        json_path = utils.get_response_json_path("putEtl", f"erid_{erid}")
        data = {}
        if response.status_code != 204 and response.text.strip():
            try:
                data = response.json()
            except ValueError:
                logging.warning("No valid JSON in the response body.")

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"✅ PUT successful {erid}")

    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = response.json()
        except Exception:
            error_body = response.text

        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ PUT failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ PUT failed (check log)")
