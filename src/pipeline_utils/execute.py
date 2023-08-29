# Selenium Web Scraping
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import logging
import pandas as pd

from src.pipeline_utils import BurpleExtract, get_links_to_items, dismiss_ads

def main():
    # setting up options
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=chrome_options)
    service = Service(executable_path='C://Users//Joanna//Desktop//Projects//Food-Explorer//chromedriver-win64//chromedriver.exe')
    driver = webdriver.Chrome(options=chrome_options, service=service)

    url = "https://www.burpple.com/search/sg?q=Tampines"
    logging.info("Loading website...")
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CLASS_NAME, "container")))
    main_window = driver.current_window_handle
    dismiss_ads(driver)
    driver.switch_to.window(main_window)
    
    logging.info("Getting links to items...")
    item_links = get_links_to_items(driver)

    appended_data = []

    logging.info(f"Length of item links {len(item_links)}")
    
    for i, item_url in enumerate(item_links):
        logging.info(f"{i}: {item_url}")
        try:
            driver.get(item_url)
            dismiss_ads(driver)
            driver.switch_to.window(main_window)
            WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CLASS_NAME, "venue-details")))
        except:
            logging.info("Timeout. Attempting to refresh webpage")
            driver.refresh()

        extract = BurpleExtract(driver)
        logging.info("Extracted basic information...")

        extract.get_reviews()
        item_dict = pd.DataFrame(extract.data_dict)
        appended_data.append(item_dict)
    
    concat_data = pd.concat(appended_data)
    concat_data.to_csv("../../data/raw/data.csv", index=False, encoding='utf_8_sig')
  

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                        level=logging.INFO, 
                        filename="../../logs/logs.log", 
                        filemode="w", 
                        force=True)
    main()