import sys
import os
import time
import logging
import traceback
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils
import API.exporting_etls_config.GET_all_etls as GET_all_etls
import API.exporting_etls_config.POST_etl_configuration as POST_etl_configuration
import API.updating_etls_config.POST_etl_config as POST_etl_config  # <-- patch_etl_configuration dovrebbe trovarsi qui

def change_module():
    etls_JSON = GET_all_etls.get_all_etls()
    list_of_etls = [etl['etl_id'] for etl in etls_JSON]

    for erid in list_of_etls:
        # Recupero della configurazione ETL corrente
        response_str = POST_etl_configuration.post_etl_configuration(erid)
        if not response_str:
            continue

        try:
            details_etls = json.loads(response_str)
        except json.JSONDecodeError:
            continue

        if "etl" not in details_etls or "module_name" not in details_etls["etl"]:
            continue

        print(f"ETL {erid} module name --> {details_etls['etl']['module_name']}")

        if details_etls['etl']['module_name'] == "com.neptuny.cpit.etl.extractor.DMSQLE":
            details_etls['etl']['module_name'] = "com.neptuny.cpit.etl.loader.seriesMessagL"
            input("🔹Confirm PATCH")
            POST_etl_config.patch_etl_configuration(erid, details_etls)
            time.sleep(3)
            POST_etl_configuration.post_etl_configuration(erid)

                