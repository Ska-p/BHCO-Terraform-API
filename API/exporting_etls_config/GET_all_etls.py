import os
import sys
import json
import logging
import traceback
import requests

# Add project base path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# Load config paths
def _load_config():
    base = utils.get_base_dir()
    with open(os.path.join(base, 'config.json')) as f:
        return json.load(f)

# Load credentials
def _load_credentials():
    base = utils.get_base_dir()
    with open(os.path.join(base, 'EnvironmentCredentials', 'credentials.json')) as f:
        return json.load(f)


def get_all_etls():
    """
    Retrieves a list of all ETLs from the API.
    :return: list of ETL dicts, or None on error
    """
    cfg = _load_config()
    creds = _load_credentials()
    url = f"{creds['base_url'].rstrip('/')}/etls"
    try:
        response = requests.get(url, auth=(creds['username'], creds['password']), timeout=cfg.get('timeout', 30))
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"❌ HTTP error in GET all ETLs: {http_err}\n{traceback.format_exc()}")
    except requests.RequestException as err:
        logging.error(f"❌ Request failed in GET all ETLs: {err}\n{traceback.format_exc()}")
    return None