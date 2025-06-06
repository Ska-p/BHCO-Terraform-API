import utils
import requests
import json
import utils
import API.exporting_etls_config.GET_all_etls as GET_all_etls
import API.exporting_etls_config.POST_etl_configuration as POST_etl_configuration
import API.POST_login as POST_login
import workflows.change_scheduler as change_scheduler
import workflows.change_module as change_module
import API.datamart.retrive_datamart_data as retrive_datamart_data
import workflows.datamart_data_to_csv as datamart_data_to_csv
import workflows.domain_entities_to_csv as domain_entities_to_csv
import API.datamart.retrieve_datamart_metadata as retrieve_datamart_metadata
import API.datamart.get_datamart_summary as get_datamart_summary
import API.datamart.post_datamart_cst as post_datamart_cst
import API.datamart.post_cst_data as post_cst_data
import API.datamart.get_cst_datamart as get_cst_datamart


def start():
    utils.reset_log()
    utils.remove_pycache()
    utils.setup_logging()
    POST_login.login()

if __name__ == "__main__":
    start()
    #datamart_data_to_csv.convert_datamart_json_to_csv()
    retrieve_datamart_metadata.get_datamart_metadata(3569)
    #get_datamart_summary.get_datamart_summary(3698)
    #get_cst_datamart.get_datamart_custom_table_data(3569)

    #domain_entities_to_csv.convert_domain_entities_to_csv()