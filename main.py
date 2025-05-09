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
import API.datamart.retrive_datamart_summary as retrive_datamart_summary
import API.datamart.retrive_datamart_summary_sql as retrive_datamart_summary_sql
def start():
    utils.reset_log()
    utils.remove_pycache()
    utils.setup_logging()
    POST_login.login()
    

if __name__ == "__main__":
    start()
    datamart_data_to_csv.convert_datamart_json_to_csv()