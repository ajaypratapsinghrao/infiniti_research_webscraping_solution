from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from googletrans import Translator
import json
import concurrent.futures
import time
import os

class ProductDataScraper:
    def __init__(self, option, chrome_driver_path):

        # ----------------Uncomment if using compaitable chrome version for webpage transalation-------- 
        # options.add_argument('--lang=en')
        # prefs = {
        #     "translate_whitelists": {"fr": "en"},
        #     "translate": {"enabled": "true"}
        # }
        # options.add_experimental_option("prefs", prefs)
        # -------------------------------------------------------------------------------------------------

        self.options = option
        self.chrome_driver_path = chrome_driver_path

    def run(self, url):
        try:
            print("--------------------------Starting the products data scraper.---------------------")
            with webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.options) as driver:
                driver.get(url)
                time.sleep(30)

                # Handle consent dialog if present
                self._handle_consent_dialog(driver)


                # Scrape and translate reviews
                try:
                    reviews_data = self._scrape_products_data(driver)
                except Exception as e:
                    print("Error occurred during scraping:", e)
                    reviews_data = []

                # Save the data to JSON file
                self._save_products_to_json(reviews_data)
                print("-------------------------- Products data scraper succeeded---------------------")
        except Exception as e:
            print("--------------------------Products Data scraper failed---------------------")
            print("Failure", e)

    def _handle_consent_dialog(self, driver):
        consent_text = "discount utilise des cookies"
        if consent_text in driver.page_source:
            print("Handling consent dialog...")
            desired_string = "Accepter"
            button = driver.find_element(By.XPATH, "//button[contains(., '" + desired_string + "')]")
            button.click()

    def _scrape_products_data(self, driver):
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        li_elements = soup.find('ul', {'id': 'lpBloc'}).find_all('li', attrs={'data-sku': True})
        products_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(li_elements)) as executor:
            extraction_futures = {executor.submit(self._extract_product_data, li_element): li_element for li_element in li_elements}
            for future in concurrent.futures.as_completed(extraction_futures):
                li_element = extraction_futures[future]
                try:
                    extracted_data = future.result()
                    products_data.append(extracted_data)
                except Exception as e:
                    print("Error occurred during extraction:", e)
                print(f"Scraped Product Data {len(products_data)} of {len(li_elements)}")
        return products_data

    def _extract_product_data(self, li_element):
            translator = Translator()
            try:
                product_link = li_element.find('a')['href']
            except AttributeError:
                product_link = ""
            try:
                product_name = li_element.find('h2', class_='prdtTit').text.strip()
            except AttributeError:
                product_name = "not available"
            try:
                price_tag = li_element.find('span', class_='price')
                price = price_tag.text.strip() if price_tag else None
                if price:
                    price = ''.join(filter(str.isdigit, price))
                product_price = price
            except AttributeError:
                product_price = ""
            try:
                total_ratings_tag = li_element.find('span', class_='c-stars-result__text')
                total_ratings = ""
                if total_ratings_tag:
                    total_ratings = total_ratings_tag.text.strip()
                product_total_ratings = total_ratings
            except (AttributeError, TypeError, KeyError):
                product_total_ratings = ""
            try:
                rating_tag = li_element.find('span', class_='u-visually-hidden')
                rating = "not available"
                if rating_tag:
                    rating = rating_tag.text.strip()
                product_rating = rating
            except (AttributeError, TypeError, KeyError):
                product_rating = "not available"            

            product_data = {
                'Product Link': product_link,
                'Product Name': translator.translate(product_name).text,
                'Product Price': product_price,
                'Product Total Ratings': product_total_ratings,
                'Product Rating': translator.translate(product_rating).text
            }
            return product_data

    def _save_products_to_json(self, product_data):
        folder_name = "scraped_data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, 'products_data.json')

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(product_data, json_file, ensure_ascii=False, indent=4)

        print(f"Product Data has been saved to '{file_path}' successfully.")




