from preprocessors.variables import *
from tqdm import tqdm, trange
import pandas as pd
import math
import re
import swifter

tqdm.pandas()

def drop_duplicate(dataframe):
    dataframe.drop_duplicates(subset=["id"], inplace=True)
    return dataframe

def lower_col_names(dataframe):
    dataframe.columns = dataframe.columns.map(lambda x: x.lower())
    return dataframe

def merge_title_text(dataframe):
    dataframe["title_text"] = dataframe.title + " " + dataframe.abstract
    return dataframe

def unify_affiliation_format(dataframe):
    def extract_affiliation_nation(series):
        result_dict = {
            "affiliations": [],
            "nations": []
        }
        arr = list(series)
        for i in trange(len(arr)):
            affiliation = []
            nation = []
            for j in range(len(arr[i])):
                affiliation.append(arr[i][j].split(",")[0].strip())
                nation.append(arr[i][j].split(",")[-1].strip())
            result_dict["affiliations"].append(" | ".join(affiliation))
            result_dict["nations"].append(" | ".join(nation))
        return result_dict

    def merge_affiliation_nation(dataframe, series_affiliations_nations_paper):
        affiliations_nations_paper_splited = extract_affiliation_nation(series_affiliations_nations_paper)
        affiliations_paper = pd.Series(affiliations_nations_paper_splited["affiliations"]).astype(str).replace({"['']": ""})
        nations_paper = pd.Series(affiliations_nations_paper_splited["nations"]).astype(str).replace({"['']": ""})
        affiliations_patent = dataframe.affiliations_patents
        nations_patent = dataframe.nation_patents
        dataframe["affiliation"] = affiliations_patent + affiliations_paper
        dataframe["nation"] = nations_patent + nations_paper
        return dataframe

    dataframe = dataframe.replace({math.nan: ""})
    affiliations_nations_paper = dataframe.affiliations_papers
    affiliations_nations_paper = (
        affiliations_nations_paper
        .progress_map(lambda x: re.sub(pat_authors, "", str(x)))
        .progress_map(lambda x: x.split(";"))
    )
    dataframe = merge_affiliation_nation(dataframe, affiliations_nations_paper)
    return dataframe

def drop_columns(dataframe):
    drop_columns = ["no", "id", "title", "abstract", 
    "affiliations_patents", "nation_patents", "affiliations_papers", 
    "categories"]
    dataframe.drop(columns = drop_columns, inplace=True)
    return dataframe

def drop_rows(dataframe):
    dataframe = dataframe[dataframe.title_text.swifter.apply(lambda x: len(x) > 1)].reset_index(drop=True)
    return dataframe

def sort_columns(dataframe):
    col_order = ["type", "application/published year", "title_text", 
    "title_text_cleansed", "title_text_tokenized", "affiliation", "nation"]
    dataframe = dataframe[col_order]
    return dataframe
