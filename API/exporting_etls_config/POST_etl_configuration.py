import os
import sys
import json
import logging
import traceback
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

def _load_config():
    base = utils.get_base_dir()
    with open(os.path.join(base, 'config.json')) as f:
        return json.load(f)

def _load_credentials():
    base = utils.get_base_dir()
    with open(os.path.join(base, 'EnvironmentCredentials', 'credentials.json')) as f:
        return json.load(f)

def post_etl_configuration(etl_id: int, payload: dict):
    """
    Posts a new configuration for a given ETL.
    :param etl_id: ID of the ETL to configure
    :param payload: configuration dict
    """
    cfg = _load_config()
    creds = _load_credentials()
    url = f"{creds['base_url'].rstrip('/')}/etls/{etl_id}/config"
    try:
        response = requests.post(
            url,
            auth=(creds['username'], creds['password']),
            json=payload,
            timeout=cfg.get('timeout', 30)
        )
        response.raise_for_status()
        logging.info(f"✅ POST ETL {etl_id} configuration applied")
        return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"❌ HTTP error in POST ETL config: {http_err}\nBody: {response.text}\n{traceback.format_exc()}")
    except requests.RequestException as err:
        logging.error(f"❌ Request failed in POST ETL config: {err}\n{traceback.format_exc()}")
    return None