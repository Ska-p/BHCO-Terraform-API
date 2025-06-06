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
    GET /opt/api/v1/datamartservice/datamarts/{erid}/summary
    Restituisce la definizione (metadati) del DataMart.
    """
    # Carica configurazione e credenziali
    config      = utils.load_config()
    creds       = utils.load_credentials()
    # Imposta il logging
    utils.setup_logging()

    logging.info(f"🔹 Starting get_datamart_summary for ERID: {datamart_id}")

    token = config.get("auth", {}).get("BearerToken")
    if not token:
        logging.error("❌ BearerToken mancante in config.json")
        print("❌ GET summary failed (check log)")
        return None

    url = f"{creds['base_url'].rstrip('/')}/opt/api/v1/datamartservice/datamarts/{datamart_id}/summary"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept":        "application/json"
    }

    logging.info(f"🔹 GET Request URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=config.get("timeout", 30))
        logging.info(f"🔹 Response Code: {response.status_code}")
        response.raise_for_status()

        summary = response.json()
        logging.info("✅ Summary received:")
        logging.info(json.dumps(summary, indent=2))

        # Salva il JSON di risposta
        path = utils.get_response_json_path("getDatamartSummary", f"datamart_{datamart_id}_summary")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        logging.info(f"✅ Summary saved to: {path}")

        print(f"✅ GET summary successful: {path}")
        return summary

    except requests.HTTPError as he:
        body = ""
        try:
            body = response.text
        except:
            pass
        logging.error(f"❌ HTTPError: {he}\nResponse Body:\n{body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET summary failed (check log)")

    except requests.RequestException as re:
        logging.error(f"❌ RequestException: {re}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ GET summary failed (check log)")

    return None