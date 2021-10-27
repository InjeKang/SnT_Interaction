from bs4 import BeautifulSoup
from scrapers.variables import *
from scrapers.get_urls import *
from tqdm import trange
from glob import glob
import time
import requests

def get_item_dom(item_urls):
    driver = load_webdriver()
    result_dict = {
            "dom": [],
            "url": []
        }
    for i in trange(len(item_urls)):
        driver.get(item_urls[i])
        time.sleep(max_pause)
        if i == 0:
            for i in range(2):
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(min_pause)
        res = driver.page_source
        result_dict["dom"].append(res)
        result_dict["url"].append(item_urls[i])
    driver.quit()
    return result_dict

def export_items(item_urls):
    driver = load_webdriver()
    for i in range(len(item_urls)):
        driver.get(item_urls[i])
        time.sleep(max_pause)
        for i in range(2):
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(min_pause)
        checkbox = driver.find_element_by_xpath(checkbox_xpath); checkbox.click(); time.sleep(min_pause)
        export_dropdown = driver.find_element_by_xpath(export_dropdown_xpath); export_dropdown.click(); time.sleep(min_pause)
        export_excel_button = driver.find_element_by_xpath(export_excel_button_xpath); export_excel_button.click(); time.sleep(random_pause_time)
        record_contents = driver.find_element_by_xpath(record_contents_xpath); record_contents.click(); time.sleep(min_pause)
        record_contents_detail = driver.find_element_by_xpath(record_contents_detail_xpath); record_contents_detail.click(); time.sleep(min_pause)
        export_button = driver.find_element_by_xpath(export_button_xpath); export_button.click(); time.sleep(min_pause)
    driver.quit()
    return 
        
