from preprocessors.variables import *
from preprocessors import multiprocess as mp
from multiprocessing import cpu_count
from sklearn.feature_extraction.text import TfidfVectorizer
from keybert import KeyBERT
from math import nan
import preprocessors.helper as help
import pandas as pd
import numpy as np
import re
import spacy
import swifter
import itertools
# import cudf

def cleanse_text(dataframe):
    def extract_pos(text, nlp):
        try:
            text_nlp = nlp(text)
            extracted_text = " ".join([token.lemma_ for token in text_nlp if bool(re.match(pat_pos, token.tag_)) == True])
        except ValueError: 
            extracted_text = ""
        return extracted_text

    def remove_stopwords(text):
        stopword_removed_text = " ".join([token for token in text.split(" ") if bool(re.match(pat_stopwords, token)) == False])
        return stopword_removed_text
    
    title_text_cleansed = dataframe.title_text
    spacy.require_gpu()
    nlp = spacy.load("en_core_web_md")

    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: x.lower())
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_punc_replace, " ", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_stopwords, "", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_tags, "", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_paths, "", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_emails, "", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: extract_pos(x, nlp))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_punc_remove, " ", x))
    title_text_cleansed = title_text_cleansed.swifter.apply(lambda x: re.sub(pat_whitespaces, "", x))
    dataframe["title_text_cleansed"] = title_text_cleansed
    return dataframe

def get_bert_keyword(dataframe):
    kw_model = KeyBERT("all-mpnet-base-v2")
    # title_text_pooled = " ".join(dataframe.title_text_cleansed)
    # keywords_list = kw_model.extract_keywords(title_text_pooled, keyphrase_ngram_range=(1,3), top_n = 500, stop_words="english")
    # keywords_df = pd.DataFrame(keywords_list, columns=["word", "score"]).sort_values(by=["score"], ascending=False).drop_duplicates(subset=['word']).reset_index(drop=True)
    title_text_keywords = dataframe.title_text_cleansed.swifter.apply(lambda x: kw_model.extract_keywords(x, keyphrase_ngram_range=(1,3), stop_words="english", top_n=10))
    keywords_list = help.concat_list(title_text_keywords)
    keywords_df = pd.DataFrame(keywords_list, columns=["word", "score"]).sort_values(by=["score"], ascending=False).drop_duplicates(subset=['word']).reset_index(drop=True)
    return keywords_df

def replace_keywords(dataframe, user_dict):
    title_text = dataframe.title_text_cleansed.copy()
    title_text_replaced = mp.multiprocess_keyword_replace(title_text, user_dict, mp.replace_df)
    # title_text_cudf = cudf.Series.from_pandas(title_text)
    # title_text_replaced = title_text_cudf.replace(dict, regex=True)
    dataframe["title_text_replaced"] = title_text_replaced
    return dataframe

def tokenize(dataframe):
    try:
        title_text = dataframe.title_text_replaced
    except AttributeError:
        title_text = dataframe.title_text_cleansed
    title_text_tokenized = title_text.swifter.apply(lambda x: x.split() if type(x) != nan else nan)
    dataframe['title_text_tokenized'] = title_text_tokenized
    return dataframe