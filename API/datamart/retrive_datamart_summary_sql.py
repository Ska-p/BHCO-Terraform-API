
import os
import sys
import json
import requests
import logging
import traceback

# Add project base path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

def post_datamart_summary_properties(byerid: str = None):
    """
    POST /opt/api/v1/datamartservice/datamarts/summary
    Popola le proprietà del Summary DataMart a partire dall'ID di un DataMart SQL.

    @param byerid: ID del DataMart SQL da cui generare il summary.
                   Se non fornito, prova a leggerlo da `config.json` sotto `datamart.byerid`.
    """
    # Carica config e credenziali, setup logging
    config      = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    logging.info(f"🔹 Starting post_datamart_summary_properties for SQL ERID: {byerid}")

    # Determina byerid
    if not byerid:
        byerid = config.get("datamart", {}).get("byerid")
        if not byerid:
            logging.error("❌ SQL DataMart ID (byerid) mancante! Inseriscilo come parametro o in config.json.")
            print("❌ POST summary properties failed (check log)")
            return None

    # Recupera token
    token = config.get("auth", {}).get("BearerToken")
    if not token:
        logging.error("❌ BearerToken mancante in config.json. Effettua prima il login.")
        print("❌ POST summary properties failed (check log)")
        return None

    # Costruisci URL, headers e payload
    url = f"{credentials['base_url'].rstrip('/')}/opt/api/v1/datamartservice/datamarts/summary"
    headers = {
        "Content-Type":  "application/json",
        "Accept":        "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Esempio di payload di summary: include ora il campo "name" obbligatorio
    payload = {
        "byerid": int(byerid),
        "name": f"Summary of SQL DataMart {byerid}",
        "description": f"Auto-generated summary for SQL DataMart {byerid}"
        # Aggiungi altri campi se necessari (timefilter, columns, ecc.)
    }

    logging.info(f"🔹 POST Request URL: {url}")
    logging.info(f"🔹 Payload: {json.dumps(payload)}")

    try:
        body = json.dumps(payload)
        response = requests.post(url, headers=headers, data=body, timeout=config.get("timeout", 30))
        logging.info(f"🔹 Response Code: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        props = data.get("summary_datamart", data)
        logging.info("✅ Summary properties received:")
        logging.info(json.dumps(props, indent=2))

        # Salva la risposta
        path = utils.get_response_json_path(
            "postDatamartSummaryProperties",
            f"sql_{byerid}_summary_props"
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"✅ Summary properties salvate in: {path}")

        print(f"✅ POST summary properties successful: {path}")
        return props

    except requests.HTTPError as he:
        body = response.text if 'response' in locals() else ""
        logging.error(f"❌ HTTPError: {he}\nResponse Body:\n{body}")
        logging.error(f"🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST summary properties failed (check log)")

    except requests.RequestException as re:
        logging.error(f"❌ RequestException: {re}\n🔹 Full Traceback:\n{traceback.format_exc()}")
        print("❌ POST summary properties failed (check log)")

    return None