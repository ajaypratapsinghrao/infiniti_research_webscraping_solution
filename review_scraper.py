from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from googletrans import Translator
import json
import concurrent.futures
import os
import time

class ReviewScraper:
    def __init__(self, option, chrome_driver_path):

        # ----------------Uncomment if using compaitable chrome version for webpage transalation-------- 
        # options.add_argument('--lang=en')
        # prefs = {
        #     "translate_whitelists": {"cs": "en"},
        #     "translate": {"enabled": "true"}
        # }
        # options.add_experimental_option("prefs", prefs)
        # -------------------------------------------------------------------------------------------------

        self.options = option
        self.chrome_driver_path = chrome_driver_path

    def run(self, url):
        try:
            print("--------------------------Starting the reviews scraper.---------------------")
            with webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.options) as driver:
                driver.get(url)
                time.sleep(30)

                # Handle consent dialog if present
                self._handle_consent_dialog(driver)

                # Go to the reviews section
                anchor_tag = driver.find_element(By.XPATH, "//a[contains(., 'Recenze')]")
                anchor_tag.click()

                # Scrape and translate reviews
                try:
                    reviews_data = self._scrape_reviews(driver)
                except Exception as e:
                    print("Error occurred during scraping:", e)
                    reviews_data = []

                # Save the data to JSON file
                self._save_reviews_to_json(reviews_data)
                print("-------------------------- Reviews scraper succeeded---------------------")
        except Exception as e:
            print("--------------------------Reviews scraper failed---------------------")
            print("Failure", e)

    def _handle_consent_dialog(self, driver):
        consent_text = "Do you consent to our use of cookies, please?"
        if consent_text in driver.page_source:
            print("Handling consent dialog...")
            desired_string = "Agree and close"
            button = driver.find_element(By.XPATH, "//button[contains(., '" + desired_string + "')]")
            button.click()

    def _scrape_reviews(self, driver):
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        li_elements = soup.find_all('li', class_='c-box-list__item c-post')
        
        reviews_data = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(li_elements)) as executor:
            extraction_futures = {executor.submit(self._extract_review_data, li_element): li_element for li_element in li_elements}
            for future in concurrent.futures.as_completed(extraction_futures):
                li_element = extraction_futures[future]
                try:
                    extracted_data = future.result()
                    reviews_data.append(extracted_data)
                except Exception as e:
                    print("Error occurred during extraction:", e)
                print(f"Scraped review {len(reviews_data)} of {len(li_elements)}")
        return reviews_data

    def _extract_review_data(self, li_element):
            translator = Translator()
            try:
                review_title = li_element.find('p', class_='c-post__author').text.strip()
            except AttributeError:
                review_title = ""
            try:
                review_comment = li_element.find('div', class_='c-post__content').find('p').text.strip()
            except AttributeError:
                review_comment = ""
            try:
                review_date = li_element.find('time', class_='c-post__publish-time').text.strip()
            except AttributeError:
                review_date = ""
            try:
                purchased_at = li_element.find('p', class_='c-post__time-shop').find('span').find('a')['href']
            except (AttributeError, TypeError, KeyError):
                purchased_at = ""

            return {
                'Review Title': translator.translate(review_title).text,
                'Review Date': translator.translate(review_date).text,
                'Review Comments': translator.translate(review_comment).text,
                'Purchased At': purchased_at,
            }

    def _save_reviews_to_json(self, reviews_data):
        folder_name = "scraped_data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, 'reviews_data.json')

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(reviews_data, json_file, ensure_ascii=False, indent=4)

        print(f"Reviews Data has been saved to '{file_path}' successfully.")
