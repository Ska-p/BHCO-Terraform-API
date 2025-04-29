import requests
import json
import utils
import logging
import traceback

def patch_etl_configuration(etl_id: str = None,
                           new_properties: dict = None,
                           properties_to_delete: dict = None):
    """
    Aggiorna parzialmente le proprietà di un ETL, usando l'endpoint:
    POST /opt/api/v1/backend/etls/<etl-id>/configuration/update

    :param etl_id:            ID dell’ETL da modificare (se non fornito, preso da config.json)
    :param new_properties:    Proprietà da aggiungere o aggiornare (dict: chiave -> nuovo valore)
    :param properties_to_delete: Proprietà da cancellare (dict: chiave -> valore qualunque)
    """

    # Carica config e logging
    config = utils.load_config()
    utils.setup_logging()
    credentials = utils.load_credentials()
    # 1) Recupero ETL ID, se non specificato
    if etl_id is None:
        etl_id = config.get("etl", {}).get("erid")
        if etl_id is None:
            logging.error("❌ ETL ID non fornito né presente in config.json.")
            print("❌ Patch failed (check log)")
            return

    # 2) Recupero Bearer Token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ Nessun Bearer Token. Esegui prima il login.")
        print("❌ Patch failed (check log)")
        return

    # 3) Preparazione corpo richiesta
    payload = {
        "encryption_passphrase": config.get("auth", {}).get("encryption_passphrase", None)
    }

    if new_properties:
        payload["properties"] = new_properties

    if properties_to_delete:
        payload["properties_to_delete"] = properties_to_delete

    url = f"{credentials['base_url']}/opt/api/v1/backend/etls/{etl_id}/configuration/update"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 4) Invio richiesta
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        logging.info(f"✅ PATCH su ETL {etl_id} eseguito correttamente. (Status code: {response.status_code})")
        logging.info(f"Response Body:\n{response.text}")

        print(f"✅ Patch eseguita su ETL {etl_id}.")
    except requests.HTTPError as http_err:
        logging.error(f"❌ HTTPError: {http_err}")
        print("❌ Patch failed (check log)")
        try:
            logging.error(f"Body di risposta:\n{response.text}")
        except:
            pass
    except requests.RequestException as e:
        logging.error(f"❌ RequestException: {e}")
        print("❌ Patch failed (check log)")
        logging.error(f"Traceback:\n{traceback.format_exc()}")
