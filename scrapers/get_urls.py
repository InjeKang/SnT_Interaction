from scrapers.variables import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from tqdm import trange
import time
import numpy as np

def load_webdriver():
    webdriver_options = webdriver.ChromeOptions()
    for arg in webdriver_option_args:
        webdriver_options.add_argument(arg)
    webdriver_options.add_experimental_option('prefs', webdriver_pref)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=webdriver_options)
    driver.set_window_position(-2000, 0)
    driver.maximize_window()
    return driver

def scan_page(driver):
    continue_scroll = True
    while continue_scroll == True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(min_pause*2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            continue_scroll = False
    for stride in np.linspace(new_height, 0, 50):
        driver.execute_script(f"window.scrollTo(0, {stride});")
        time.sleep(min_pause)
    return

def get_query_urls():
    driver = load_webdriver()
    driver.get(url_query(1))
    popup_exists = True
    while popup_exists == True:
        try:
            max_page_num = int(driver.find_elements_by_xpath(max_page_num_xpath)[0].text.replace(",",""))
            if type(max_page_num) == int:
                popup_exists = False
        except:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    page_range = range(1, max_page_num+1)
    url_queries = [url_query(page) for page in page_range]
    driver.quit()    
    return url_queries

def get_page_url(url_queries):
    result_dict = {
            "dom": [],
            "url": []
        }
    driver = load_webdriver()
    for i in range(len(url_queries)):
        driver.get(url_queries[i])
        res_txt = driver.page_source
        result_dict["dom"].append(res_txt)
        result_dict["url"].append(url_queries[i])
    return result_dict

def get_item_urls(url_queries):
    result_dict = {
            "title": [],
            "url": []
        }
    driver = load_webdriver()
    for i in trange(len(url_queries)):
        driver.get(url_queries[i])
        scan_page(driver)
        items_by_page = driver.find_elements_by_css_selector(item_title_css)
        titles = list(map(lambda x: x.text, items_by_page))
        href = list(map(lambda x: x.get_attribute("href"), items_by_page))
        result_dict["title"].extend(titles)
        result_dict["url"].extend(href)
    driver.quit()
    return result_dict
