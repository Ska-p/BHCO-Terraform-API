import os
import json
import csv
import logging
import sys
import API.datamart.retrive_datamart_data as retrive_datamart_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import time
utils.setup_logging()

def convert_datamart_json_to_csv():
    """
    Converte la risposta JSON del Datamart (logs/response) in un CSV (logs/).
    """
    datamart_id = input("🔹 Enter Datamart ID to convert to CSV: ")
    retrive_datamart_data.post_datamart_data(datamart_id)

    json_path = utils.get_response_json_path("postDatamartData", f"datamart_{datamart_id}")
    input("Modifica nel json quello che devi modificare")
    if not os.path.exists(json_path):
        logging.error(f"❌ JSON file not found at {json_path}")
        print("❌ JSON file not found (check log)")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        json_content = json.load(f)

    data = json_content.get("data", [])
    if not data:
        logging.error("❌ No 'data' section found inside the JSON.")
        print("❌ No data found inside JSON (check log)")
        return

    # Costruiamo l'elenco di tutte le colonne
    all_keys = set()
    for record in data:
        all_keys.update(record.keys())
    fieldnames = sorted(all_keys)

    csv_path = os.path.join(utils.get_logs_dir(), f"Datamart_{datamart_id}.csv")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"✅ CSV file generated successfully at {csv_path}")
        print(f"✅ CSV generated: {csv_path}")

    except Exception as e:
        logging.error(f"❌ Error processing JSON to CSV: {e}\n{traceback.format_exc()}")
        print("❌ Error during conversion (check log)")

