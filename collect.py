from scrapers import get_urls as url
from scrapers import get_metadata as md
from scrapers import multiprocessor as mp
from scrapers import helper
from scrapers.variables import *
from glob import glob
import os
import pandas as pd

# Path
wd_current = os.getcwd()
download_path = os.path.join(wd_current, "data", "collection", "exported")

def collect():
    # Working directory
    wd_current = os.getcwd()
    wd_data = os.path.join(wd_current, "data")
    os.chdir(wd_data)
    # Switches
    page_url = True
    item_export = True
    item_merge = True
    # Get page url
    if page_url == False:
        url_queries = url.get_query_urls()
        query_dom = mp.multiprocess_function(url_queries, url.get_page_url)
        query_dom_df = help.multiprocessing_into_dataframe(query_dom)
        query_dom_df.to_csv("query_dom.csv", encoding="utf-8-sig")
        query_dom_df.to_pickle("query_dom")
    # Automate exportation
    if item_export == False:
        page_url = list(pd.read_pickle("query_dom")["url"])
        path = os.path.join(download_path, "*.xls")
        for file in glob(path):
            os.remove(file)
        mp.multiprocess_function(page_url, md.export_items)
    # Merge files
    if item_merge == False:
        data_df = helper.merge_excel(download_path)
        data_df.to_csv("data.csv", encoding="utf-8-sig", index=False)
        data_df.to_pickle("data")
    return 

# Kick off the program
if __name__ == "__main__":
    collect()