import os
import json
import logging
import requests
import traceback
import utils


def login():
    """
    Authenticates with the Unicredit API and retrieves an access token.

    @return: The response object from the API request.

    Requirements:
    - `EnivironmentCredentials/UnicreditCredentials.json` must contain:
        - `tenant_id`: The tenant identifier.
        - `access_key`: The API access key.
        - `access_secret_key`: The API secret key.
    - Logging is configured via `utils.setup_logging()`.
    - The API response should contain `json_web_token`, which will be stored in `config.json`.

    Raises:
    - Logs an error if the credentials file is missing or incorrectly formatted.
    - Logs an error if the API request fails.
    """

    # ✅ Setup Logging
    utils.setup_logging()

    # ✅ Load Credentials
    credentials_path = os.path.join(utils.get_base_dir(), 'EnvironmentCredentials', 'credentials.json')
    try:
        with open(credentials_path) as f:
            credentials = json.load(f)
        logging.info("✅ Credentials successfully loaded.")
    except Exception as e:
        logging.error(f"❌ Error loading credentials: {e}")
        print("❌ Login failed (check log)")
        return None
    credentials["base_url"]
    # ✅ API Endpoint
    url = f"{credentials["base_url"]}/ims/api/v1/access_keys/login"

    # ✅ Construct Request Data
    payload = {
        "tenant_id": credentials["tenant_id"],
        "access_key": credentials["access_key"],
        "access_secret_key": credentials["access_secret_key"]
    }

    headers = {'Content-Type': 'application/json'}

    # ✅ Log request details
    logging.info(f"🔹 POST Request URL: {url}")
    logging.info(f"🔹 POST Headers: {headers}")
    logging.info(f"🔹 POST Payload: {json.dumps(payload, indent=4)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # ✅ Log full response
        logging.info(f"✅ Login request completed successfully!")
        logging.info(f"✅ Response Code: {response.status_code}")
        logging.info(f"✅ Response Body:\n{response.text}")

        # ✅ Extract token from response
        data = response.json()
        token = data.get("json_web_token")

        if token:
            # ✅ Save Token in Config
            config = utils.load_config()
            config.setdefault("auth", {})["BearerToken"] = token
            utils.save_config(config)
            logging.info("✅ Token successfully saved in config.json")
            print("✅ Login successful")
            return response
        else:
            logging.warning("⚠️ No token received from the API response")
            print("❌ Login failed (check log)")
            return None

    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = response.json()  # Attempt to extract JSON response
        except Exception:
            error_body = response.text  # If JSON parsing fails, log raw text

        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ Login failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ Login failed (check log)")

    return None
