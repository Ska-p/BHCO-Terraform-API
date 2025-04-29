import os
import requests
import logging
import json
import traceback
import utils


def get_all_etls():
    """
    Retrieves a list of all ETLs from the API.

    @return: A list of ETL processes as dictionaries.

    Requirements:
    - `config.json` must contain:
        - `auth.BearerToken`: The authentication token.
    - Logging is configured via `utils.setup_logging()`.
    - The API response is saved in `logs/response/`.

    Raises:
    - Logs an error if `BearerToken` is missing.
    - Logs an error if the API request fails.
    """

    # ✅ Load Configuration & Setup Logging
    config = utils.load_config()
    utils.setup_logging()

    # ✅ Retrieve Bearer Token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ GET failed (check log)")
        return None

    url = "https://unicreditcapacity-itom-dev.onbmc.com/opt/api/v1/backend/etls/"

    headers = {'Authorization': f'Bearer {token}'}

    # ✅ Log request details
    logging.info(f"🔹 GET Request URL: {url}")
    #logging.info(f"🔹 GET Headers: {headers}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # ✅ Log full response
        logging.info("✅ GET request completed successfully!")
        logging.info(f"✅ Response Code: {response.status_code}")
        logging.info(f"✅ Response Body:\n{response.text}")

        # ✅ Save response JSON
        json_path = utils.get_response_json_path("getEtl", "success")
        with open(json_path, 'w') as f:
            json.dump(response.json(), f, indent=4)

        print("✅ GET successful")
        return response.json()

    except requests.HTTPError as http_err:
        error_message = f"❌ API Request Error: {http_err}"
        try:
            error_body = response.json()  # Attempt to extract JSON response
        except Exception:
            error_body = response.text  # If JSON parsing fails, log raw text

        logging.error(f"{error_message}\nResponse Body:\n{error_body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET failed (check log)")

    except requests.RequestException as e:
        error_message = f"❌ Network/API request failed: {e}"
        logging.error(f"{error_message}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET failed (check log)")

    return None
