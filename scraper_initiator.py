from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from product_scraper import ProductDataScraper
from review_scraper import ReviewScraper
import os

class ScraperInitiator:
    def __init__(self):
        self.options = Options()
        # -----------------Uncomment if vpn connection is not available-----------
        # proxy_ip_port = os.environ["PROXY_SERVER_IP_PORT"]
        # self.options.add_argument(f'--proxy-server={proxy_ip_port}')
        # ---------------------------------------------------------------------------

        self.options.add_argument("-incognito")
        self.chrome_driver_path = os.environ["CHROME_DRIVER_PATH"]
        self.product_data_scraper = ProductDataScraper(self.options, self.chrome_driver_path)
        self.review_scraper = ReviewScraper(self.options, self.chrome_driver_path)
        
    def run(self):
        print("--------------------------Setting up scraper initiator---------------------")
        url_to_scraper = { 
            "product_url": "https://cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html", 
             "review_url": "https://susicky.heureka.cz/aeg-absolutecare-t8dee68sc/"
             }
        
        self.product_data_scraper.run(url_to_scraper["product_url"])
        self.review_scraper.run(url_to_scraper["review_url"])

if __name__ == "__main__":
    scraper_initiator = ScraperInitiator()
    scraper_initiator.run()


