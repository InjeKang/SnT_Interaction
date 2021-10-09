from preprocessors import external as ext
from preprocessors import internal as int
from preprocessors import dictionary as dic
from tqdm import tqdm
import pandas as pd
import os

# Setting working directory
wd_current = os.getcwd()
work_path = os.path.join(wd_current, "data", "cleansing")

external = True
internal = False
keyword_extraction = False
keyword_registration = True

def preprocess():
    # Working Directory
    os.chdir(work_path)
    raw_data = pd.read_excel("raw_data.xlsx")
    # External manipulation
    if external == False:
        data = ext.lower_col_names(raw_data)
        data = ext.drop_duplicate(data)
        data = ext.merge_title_text(data)
        data = ext.unify_affiliation_format(data)
        data = ext.drop_columns(data)
        data = ext.drop_rows(data)
        data.to_pickle("data_temp_ext")
        data.to_excel("data_temp_ext.xlsx")
    # Internal manipulation
    if internal == False:
        data = pd.read_pickle("data_temp_ext")
        data = int.cleanse_text(data)
        #data.to_pickle("data_temp_int")
        #data.to_excel("data_temp_int.xlsx")
    if keyword_extraction == False:
        data = pd.read_pickle("data_temp_int")
        keywords = int.get_bert_keyword(data)
        #keywords.to_excel("keywords.xlsx")
        #keywords.to_pickle("keywords")
    if keyword_registration == False:
        keywords, data = pd.read_pickle("keywords"), pd.read_pickle("data_temp_int")
        user_dict, user_dict_df = dic.user_dict_creator(keywords)
        user_dict_df.to_excel("user_dict.xlsx")
        data = int.replace_keywords(data, user_dict)
        data = int.tokenize(data)
        data = ext.sort_columns(data)
        data.to_pickle("data_final")
        data.to_excel("data_final.xlsx")

if __name__ == "__main__":
    preprocess()

    
    