from scrapers.variables import *
from tqdm import trange
from multiprocessing import Pool, cpu_count

def multiprocess_function(arr, target_func):
    pool = Pool()
    results = []
    ITERATION_COUNT = cpu_count() - 1
    count_per_iteration = len(arr) / float(ITERATION_COUNT)
    for i in trange(ITERATION_COUNT):
        time.sleep(random_pause_time)
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        results.append(pool.apply_async(target_func, (arr[list_start:list_end],)))
    pool.close()
    pool.join()
    time.sleep(random_pause_time)
    results_val = [results[i].get() for i in range(len(results)) if results[i].successful()]
    return results_val