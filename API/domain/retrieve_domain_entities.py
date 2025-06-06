import requests
import json
import logging
import traceback
import sys
import os

# Add the project base path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

# Funzione per ottenere le entità del dominio
def get_subdomains(domain_id: str = None):

    # Load configuration and setup logging
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    # Retrieve domain_id if not passed
    if domain_id is None:
        domain_id = config.get("domain", {}).get("domain_id", None)
        if domain_id is None:
            logging.error("❌ Domain ID not found! Provide it as a parameter or add it to `config.json`.")
            print("❌ GET failed (check log)")
            return

    # Retrieve token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ No Bearer Token found! Please log in using `POST_login.py`.")
        print("❌ GET failed (check log)")
        return

    url = f"{credentials["base_url"]}/opt/api/v1/catalog/explore/domains/{domain_id}/tree"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        "group": "all", # Sostituisci "all" con il valore appropriato per il tuo caso
        "depth": -1
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"❌ Errore HTTP: {http_err}")
        logging.error(f"🔹 Corpo della risposta: {response.text}")
        logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
        exit(1)
    except requests.RequestException as e:
        logging.error(f"❌ Errore nella richiesta: {e}")
        logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
        exit(1)

def get_entity_tree(entity_id):
    # Carica la configurazione e le credenziali
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    # Recupera il token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ Nessun Bearer Token trovato! Effettua il login utilizzando `POST_login.py`.")
        print("❌ GET fallita (controlla il log)")
        return

    url = f"{credentials['base_url']}/opt/api/v1/catalog/explore/entities/{entity_id}/tree"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        "group": "all",
        "depth": -1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.HTTPError as http_err:
        logging.error(f"❌ Errore HTTP: {http_err}")
        logging.error(f"🔹 Corpo della risposta: {response.text}")
        logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
        print("❌ GET fallita (controlla il log)")
    except requests.RequestException as e:
        logging.error(f"❌ Errore nella richiesta: {e}")
        logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
        print("❌ GET fallita (controlla il log)")

def apply_tag_to_entities(entity_ids):
    # Carica la configurazione e le credenziali
    config = utils.load_config()
    credentials = utils.load_credentials()
    utils.setup_logging()

    # Recupera il token
    token = config.get("auth", {}).get("BearerToken", None)
    if not token:
        logging.error("❌ Nessun Bearer Token trovato! Effettua il login utilizzando `POST_login.py`.")
        print("❌ Operazione fallita (controlla il log)")
        return

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    payload = [
        {
            "type": "Generic",
            "values": ["Italy"]
        }
    ]

    for entity_id in entity_ids:
        url = f"{credentials['base_url']}/opt/api/v1/catalog/entities/{entity_id}/tags"
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            logging.info(f"✅ Tag 'Italy' applicato con successo all'entità {entity_id}")
            print(f"✅ Tag 'Italy' applicato all'entità {entity_id}")
        except requests.HTTPError as http_err:
            logging.error(f"❌ Errore HTTP per l'entità {entity_id}: {http_err}")
            logging.error(f"🔹 Corpo della risposta: {response.text}")
            logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
            print(f"❌ Errore nell'applicazione del tag all'entità {entity_id} (controlla il log)")
        except requests.RequestException as e:
            logging.error(f"❌ Errore nella richiesta per l'entità {entity_id}: {e}")
            logging.error(f"🔹 Traceback completo:\n{traceback.format_exc()}")
            print(f"❌ Errore nella richiesta per l'entità {entity_id} (controlla il log)")

def extract_entity_ids(tree, entity_ids=None, skip_root=True):
    """
    Estrae ricorsivamente gli ID delle entità da una struttura ad albero JSON,
    con la possibilità di saltare il nodo radice.

    :param tree: La struttura ad albero JSON (dict o list).
    :param entity_ids: Lista accumulativa degli ID delle entità.
    :param skip_root: Booleano che indica se saltare il nodo radice.
    :return: Lista degli ID delle entità.
    """
    if entity_ids is None:
        entity_ids = []

    if isinstance(tree, dict):
        if not skip_root:
            entity_id = tree.get('entity_id')
            if entity_id:
                entity_ids.append(entity_id)
        children = tree.get('children', [])
        for child in children:
            extract_entity_ids(child, entity_ids, skip_root=False)
    elif isinstance(tree, list):
        for node in tree:
            extract_entity_ids(node, entity_ids, skip_root=False)

    return entity_ids

def extract_domain_ids(tree, domain_ids=None, skip_root=True):
    if domain_ids is None:
        domain_ids = []
    if isinstance(tree, dict):
        if not skip_root:
            entity_id = tree.get('entity_id')
            if entity_id:
                domain_ids.append(entity_id)
        children = tree.get('children', [])
        for child in children:
            extract_domain_ids(child, domain_ids, skip_root=False)
    elif isinstance(tree, list):
        for node in tree:
            extract_domain_ids(node, domain_ids, skip_root=False)
    return domain_ids