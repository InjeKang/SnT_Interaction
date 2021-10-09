import numpy as np
import pandas as pd
import time
from scrapers import helper as help
from preprocessors import multiprocess as mp
from multiprocessing import cpu_count, Pool
from tqdm import trange

def _apply_df(*args):
    df, func = args
    return df.apply(func)

def apply_by_multiprocessing(df, func):
    cores = cpu_count() - 1
    pool = Pool(processes = cores)
    result = pool.map(_apply_df, [(sub_df, func) for sub_df in np.array_split(df, cores)])
    pool.close()
    pool.join()
    result_df = pd.concat(result)
    return result_df

def replace_df(series, dict):
    # cudf_series = cudf.Series.from_pandas(series)
    # cudf_series_replaced = cudf_series.replace(dict, regex=True)
    series_replaced = series.replace(dict, regex=True)
    return series_replaced

def multiprocess_keyword_replace(series, dict, target_func):
    pool = Pool()
    results = []
    iteration_count = int(cpu_count()*.9)
    count_per_iteration = len(series) / float(iteration_count)
    for i in trange(iteration_count):
        time.sleep(1)
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        results.append(pool.apply_async(target_func, (series.iloc[list_start:list_end], dict)))
    pool.close()
    pool.join()
    results_val = [results[i].get() for i in range(len(results)) if results[i].successful()]
    results_df = help.multiprocessing_into_dataframe(results_val)
    return results_df