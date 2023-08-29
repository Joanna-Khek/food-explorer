# Selenium Web Scraping
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import logging

def load_more_items(driver):
    status = True
    while status:
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)  
        time.sleep(4)
        try:
            driver.find_elements(By.ID, "masonryViewMore-link")[0].click()
            logging.info("Found more items")
            time.sleep(4)
        except:
            logging.info("No more items found")
            status = False


def get_links_to_items(driver):
    # Fully load all the items
    load_more_items(driver)
    item_links = []
    # Extract the links to the items
    items = driver.find_elements(By.XPATH, "//div[@class='searchVenue card feed-item']")
    for item in items:
        link = item.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
        item_links.append(link)
    return item_links

def dismiss_ads(driver):
    try:
        logging.info("Trying to dismiss ads...")
        iframe1 = driver.find_elements(By.XPATH, "//div[@id='aswift_1_host']/iframe")[0]
        driver.switch_to.frame(iframe1)
        iframe2 = driver.find_elements(By.XPATH, "//iframe[@id='ad_iframe']")[0]
        driver.switch_to.frame(iframe2)
        driver.find_elements(By.XPATH, "//div[@id='dismiss-button']")[0].click()
    except:
        pass
        logging.info("No ads found...")

class BurpleExtract:

    def __init__(self, driver):
        self.driver = driver

        self.data_dict = dict()
        self.item_links = []

        self.data_dict["title"] = self._get_title()
        self.data_dict["num_reviews"] = self._get_num_reviews()
        self.data_dict["num_wishlisted"] = self._get_num_wishlisted()
        self.data_dict["area"] = self._get_area()
        self.data_dict["price"] = self._get_price()
        self.data_dict["tags"] = self._get_tags()
        self.data_dict["bio"] = self._get_bio()
        
    def _get_title(self):
        title = self.driver.find_elements(By.CLASS_NAME, "venue-title")[0].text
        return title
    
    def _get_num_reviews(self):
        num_reviews = self.driver.find_elements(By.CLASS_NAME, "venue-count-reviews")[0].text
        return num_reviews

    def _get_num_wishlisted(self):
        num_wishlisted = self.driver.find_elements(By.CLASS_NAME, "venue-count-wishlisted")[0].text
        return num_wishlisted

    def _get_area(self):
        area = self.driver.find_elements(By.CLASS_NAME, "venue-area")[0].text
        return area

    def _get_price(self):
        price = self.driver.find_elements(By.CLASS_NAME, "venue-price")[0].text
        return price
    
    def _get_tags(self):
        tags = self.driver.find_elements(By.CLASS_NAME, "venue-tags")[0].text
        return tags
    
    def _get_bio(self):
        bio = self.driver.find_elements(By.CLASS_NAME, "venue-bio")[0].text
        return bio
    
    def _load_more_reviews(self):
        status = True
        while status:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            try:
                self.driver.find_elements(By.ID, "load-more-reviews")[0].click()
                logging.info("Found more reviews")
                time.sleep(4)
            except:
                logging.info("No more reviews found")
                status = False

    def get_reviews(self):
        self.review_title = []
        self.review_desc = []
        self.review_image = []

        BurpleExtract._load_more_reviews(self)
        reviews_card = self.driver.find_elements(By.XPATH, "//div[@id='foodMasonry']/div[@class='food card feed-item']")
        logging.info(f"Number of reviews: {len(reviews_card)}")
                     
        if len(reviews_card) == 0:
            self.review_title.append('NA')
            self.review_desc.append('NA')
            self.review_image.append('NA')
        
        for index, card in enumerate(reviews_card):
            logging.info(f"Review Item: {index}")
            card_content = card.find_elements(By.XPATH, "//div[@class='card-body']")[index]
            image_content = card.find_elements(By.XPATH, "//div[@class='food-image']")[index]
            try:
                review_title = card_content.find_elements(By.CLASS_NAME, "food-content")[0].find_elements(By.CLASS_NAME, "food-description-title")[0].text
                self.review_title.append(review_title)
                logging.info("Review title extracted")
            except:
                logging.warning("No review title found")
                self.review_title.append('NA')

            try:
                review_desc = card_content.find_elements(By.CLASS_NAME, "food-content")[0].find_elements(By.CLASS_NAME, "food-description-body")[0].text
                self.review_desc.append(review_desc)
                logging.info("Review description extracted")
            except:
                logging.warning("No review description found, appending NA to it")
                self.review_desc.append('NA')
                
            try:
                review_image = image_content.find_elements(By.TAG_NAME, "img")[0].get_attribute("src")
                self.review_image.append(review_image)
                logging.info("Review image extracted")
            except:
                logging.warning("No review image found, appending NA to it")
                self.review_image.append('NA')
                

        logging.info(f"Length of review title: {len(self.review_title)}")
        logging.info(f"Length of review description: {len(self.review_desc)}")
        logging.info(f"Length of review image: {len(self.review_image)}")

        if len(self.review_title) == len(self.review_desc) == len(self.review_image):
            self.data_dict["review_title"] = self.review_title
            self.data_dict["review_desc"] = self.review_desc
            self.data_dict["review_image"] = self.review_image
            logging.info("Completed!")
        else:
            raise Exception("Length of review title, description and image does not match!")
        



