from collect import download_path
import random
import time
import os

# Login info
cred = {
    "email": "jsyang.michael@gmail.com",
    "pw": "Yang0904!"
}

# Login info
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

# Webdriver
webdriver_option_args = [#"--headless",
"--no-sandbox", "--disable-dev-shm-usage", "window-size=1920x1080", f"""user-agent={headers["User-Agent"]}""", "--disable-extensions", "--disable-infobars", "--disable-gpu"]
webdriver_pref = {'profile.default_content_setting_values': {'cookies' : 1, 'images': 1, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2},
"download.default_directory": download_path, 'profile.default_content_setting_values.automatic_downloads': 1, "download.prompt_for_download": False}   

# Xpath
max_page_num_xpath = "//span[@class='end-page ng-star-inserted']"
checkbox_xpath = "//*[@id='snRecListTop']//mat-checkbox"
export_dropdown_xpath = "//*[@id='snRecListTop']/app-export-menu/div/button"
export_excel_button_xpath = "//*[@id='exportToExcelButton']"
record_contents_xpath = "//button[@class='dropdown']//mat-icon"
record_contents_detail_xpath = "//div[@role='listbox' and @class='options']/div[@aria-label='상세 정보']"
export_button_xpath = "//button[@cdxanalyticsaction='Click']//span[contains(text(), '내보내기')]"

# CSS selector
max_page_num_css = "span.end-page.ng-star-inserted"
item_title_css = "a.title.title-link.font-size-18.ng-star-inserted"

# Query
url_query = lambda page: f"https://www.webofscience.com/wos/woscc/summary/8125129d-6ca3-4156-9aff-5f42406f835d-069d61d0/relevance/{page}"

# Pause time
min_pause = 1
max_pause = 3
random_pause_time = random.randrange(min_pause, max_pause)
