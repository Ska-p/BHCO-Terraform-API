import os
import json
import csv
import logging
import sys
import API.domain.retrieve_domain_entities as retrieve_domain_entities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
from datetime import datetime
import traceback
utils.setup_logging()


def convert_domain_entities_to_csv():
    domain_id = input("🔹 Enter Domain ID to convert to CSV: ")
    tree = retrieve_domain_entities.get_subdomains(domain_id)
    print(tree)

    domains = retrieve_domain_entities.extract_domain_ids(tree)

    print(domains[0])
    input()
    entities = retrieve_domain_entities.get_entity_tree(domains[0])
    print(entities)
    entities_id = retrieve_domain_entities.extract_entities(entities)
    
    input()

    retrieve_domain_entities.apply_tag_to_entities(entity_ids=entities[0])
    """
    if not entities:
        logging.info("⚠️ Nessuna entità trovata nel dominio specificato.")
        print("⚠️ Nessuna entità trovata.")
        return

    # Crea il percorso per il file CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"domain_{domain_id}_entities_{timestamp}.csv"
    csv_path = os.path.join(os.getcwd(), csv_filename)

    # Scrive i dati nel file CSV
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entities)

        logging.info(f"✅ File CSV generato con successo: {csv_path}")
        print(f"✅ CSV generato: {csv_path}")

    except Exception as e:
        logging.error(f"❌ Errore durante la scrittura del file CSV: {e}\n{traceback.format_exc()}")
        print("❌ Errore durante la generazione del CSV (vedi log)")
        
    """