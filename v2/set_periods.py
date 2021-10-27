from analyzer.variables import *
from analyzer import helper as help
from os import path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Setting working directory
wd_current = os.getcwd()
work_path = os.path.join(wd_current, "data", "cleansing")

def set_subperiod():
    data = pd.read_pickle(path.join(work_path, "data_final_main"))

    break_points = range(2000, 2019)
    data = data[(data["application/published year"] >= 2000) & (data["application/published year"] <= 2018)]

    # Split data by breakpoints
    docs = []
    for br in break_points:
        docs_by_year = " ".join(data.title_text_cleansed[data["application/published year"] == br])
        docs.append(docs_by_year)
    doc_by_periods = pd.DataFrame(data={"Period": break_points, "Text": docs})
    doc_periods = list(doc_by_periods.Period)
    doc_text = list(doc_by_periods.Text)

    # TF-IDF Similarity
    vect_tfidf = TfidfVectorizer(ngram_range=(1,1), max_features=500)
    period_term_sparse = vect_tfidf.fit_transform(doc_text)
    period_term_matrix = pd.DataFrame(data=period_term_sparse.toarray(), columns=vect_tfidf.get_feature_names(), index=doc_by_periods.Period)
    ppm_cos_tfidf = pd.DataFrame(data=cosine_similarity(period_term_matrix), columns=doc_by_periods.Period, index=doc_by_periods.Period)
    
    # Plot heatmap (TF-IDF)
    new_path = path.join(wd_current, "data", 'subperiod')
    plt.subplots(figsize=(20, 15))
    ax1 = sns.heatmap(ppm_cos_tfidf, linewidth=.05)
    ax1.set_title("Year-Year Similariy", fontsize=30)
    ax1.set_xlabel("Periods", fontsize=22)
    ax1.set_ylabel("Periods", fontsize=22)
    ax1.tick_params(labelsize=18)
    fig1 = ax1.get_figure()
    fig1.savefig(path.join(new_path, "total"))

    # Plot clustermap (TF-IDF)
    methods = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
    for method in methods:
        plt.subplots(figsize=(20, 15))
        sns.clustermap(ppm_cos_tfidf, linewidth=.05, method=method)
        # ax2.set_title("Year-Year Similariy", fontsize=30)
        # ax2.set_xlabel("Periods", fontsize=22)
        # ax2.set_ylabel("Periods", fontsize=22)
        plt.savefig(path.join(new_path, f"total_hc_{method}"))

    # # Average simiilarity calculation
    # ppm_cos_avg = ppm_cos_tfidf.mean()
    # ppm_cos_avg_cutting_point = ppm_cos_avg[ppm_cos_avg <= 0.75]
    # print(ppm_cos_avg_cutting_point)

if __name__ == "__main__":
    set_subperiod()