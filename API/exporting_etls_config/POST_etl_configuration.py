import requests
import json
import logging
import traceback
import utils


def post_etl_configuration(erid: str = None):
    """
    Sends a POST request to configure an ETL process.

    @param erid: The ETL process ID. If not provided, it will be retrieved from `config.json`.
    @return: The JSON response from the API if the request is successful, otherwise exits the program.

    Requirements:
    - `config.json` must contain:
        - `etl.erid`: The ETL ID (if not provided manually).
        - `auth.BearerToken`: The authentication token.
        - `auth.encryption_passphrase`: The encryption passphrase.
    - Logging is configured via `utils.setup_logging()`.
    - API response is saved in `logs/response/`.

    Raises:
    - Logs an error if `erid`, `BearerToken`, or `encryption_passphrase` is missing.
    - Logs an error if the API request fails.
    """

    # ✅ Load Configuration & Setup Logging
    config = utils.load_config()
    utils.setup_logging()

    # ✅ Retrieve ERID
    if erid is None:
        erid = config.get("etl", {}).get("erid", None)
        if erid is None:
            logging.error("❌ ERID not found! Provide it as a parameter or add it to `config.json`.")
            print("❌ POST failed (check log)")
            return

    # ✅ Retrieve Bearer Token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ POST failed (check log)")
        return

    # ✅ Retrieve encryption passphrase
    encrypt_pwd = config.get("auth", {}).get("encryption_passphrase", None)
    if not encrypt_pwd:
        logging.error("❌ No encryption passphrase found in `config.json`.")
        print("❌ POST failed (check log)")
        return

    url = f"https://unicreditcapacity-itom-dev.onbmc.com/opt/api/v1/backend/etls/{erid}/configuration"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # ✅ Construct payload and validate JSON
    try:
        payload = json.dumps({"encryption_passphrase": encrypt_pwd}, indent=4)
        #logging.info(f"🔹 POST Request URL: {url}")
        #logging.info(f"🔹 POST Headers: {headers}")
        #logging.info(f"🔹 POST Payload:\n{payload}")
    except TypeError as e:
        logging.error(f"❌ Failed to serialize JSON: {e}")
        print("❌ POST failed (check log)")
        return

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

        # ✅ Log full response
        logging.info(f"✅ POST ETL configuration successfully sent for ERID: {erid}")
        logging.info(f"✅ Response Code: {response.status_code}")
        #logging.info(f"✅ Response Body:\n{response.text}")

        # ✅ Save response JSON
        json_path = utils.get_response_json_path("postEtl", f"erid_{erid}")
        with open(json_path, 'w') as f:
            json.dump(response.json(), f, indent=4)

        print(f"✅ POST successful {erid}")
        return json.dumps(response.json(), indent=4)
    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = json.dumps(response.json(), indent=4)  # Attempt to extract JSON response
        except Exception:
            error_body = response.text  # If JSON parsing fails, log raw text

        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST failed (check log)")
