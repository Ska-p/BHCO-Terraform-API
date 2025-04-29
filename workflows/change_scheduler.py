import sys
import os
import time
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import API.exporting_etls_config.GET_all_etls as GET_all_etls
import API.exporting_etls_config.POST_etl_configuration as POST_etl_configuration
import API.updating_etls_config.PUT_etl_config as PUT_etl_config
import json

def change_scheduler():
    etls_JSON = GET_all_etls.get_all_etls()
    list_of_etls = [etl['etl_id'] for etl in etls_JSON]

    for erid in list_of_etls:
        response_str = POST_etl_configuration.post_etl_configuration(erid)
        if not response_str:
            continue

        try:
            details_etls = json.loads(response_str)
        except json.JSONDecodeError:
            continue

        if "scheduling" not in details_etls or "scheduler_id" not in details_etls["scheduling"]:
            continue

        if details_etls['scheduling']['scheduler_id'] != 1:
            details_etls['scheduling']['scheduler_id'] = 1
            details_etls['scheduling']['period_sec'] = 86400
            input("Confirm PUT")
            PUT_etl_config.put_etl_configuration(erid, details_etls)
            time.sleep(3)
            POST_etl_configuration.post_etl_configuration(erid)