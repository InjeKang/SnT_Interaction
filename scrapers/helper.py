from scrapers.variables import *
from glob import glob
import pandas as pd
import os

def multiprocessing_into_dataframe(data):
    data_df = pd.concat([pd.DataFrame(data[i]) for i in range(len(data))], axis=0).reset_index(drop=True)
    return data_df
    
def merge_excel(path):
    new_path = os.path.join(path, "*.xls")
    fiels_df_list = []
    files = glob(new_path)
    for file in files:
        files_df = pd.read_excel(file)
        fiels_df_list.append(files_df)
    files_df = pd.concat(fiels_df_list, axis=0).drop_duplicates()
    return files_df
