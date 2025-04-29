import os
import json
import csv
import logging
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

utils.setup_logging()

def convert_datamart_json_to_csv():
    """
    Converts a Datamart JSON response (saved in /logs/response) into a CSV file (saved in /logs).
    It asks the user for the Datamart ID to find the correct JSON file.

    @return: None
    """

    datamart_id = input("🔹 Enter Datamart ID to convert to CSV: ")

    # Path of the JSON file
    json_path = utils.get_response_json_path("postDatamartData", f"datamart_{datamart_id}")

    if not os.path.exists(json_path):
        logging.error(f"❌ JSON file not found at {json_path}")
        print(f"❌ JSON file not found (check log)")
        return

    try:
        with open(json_path, 'r') as f:
            json_content = json.load(f)

        data = json_content.get("data", [])
        if not data:
            logging.error("❌ No 'data' section found inside the JSON.")
            print(f"❌ No data found inside JSON (check log)")
            return

        csv_path = os.path.join(utils.get_logs_dir(), f"Datamart_{datamart_id}.csv")
        
        # Write CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"✅ CSV file generated successfully at {csv_path}")
        print(f"✅ CSV generated: {csv_path}")

    except Exception as e:
        logging.error(f"❌ Error processing JSON to CSV: {e}")
        print(f"❌ Error during conversion (check log)")
