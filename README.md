# INFINITI RESEARCH Web Scraping Solution

This Python application is designed to scrape product data from two websites:

1. [cdiscount.com](https://cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html)
2. [susicky.heureka.cz](https://susicky.heureka.cz/aeg-absolutecare-t8dee68sc/)

It utilizes the Selenium library for browser automation and BeautifulSoup for HTML parsing. The scraped data is then stored in a JSON file under.


# Getting Started

Connect your system to vpn connection ( Preferably : european region )

Before running the code, ensure that you have the following dependencies installed:

You can install these dependencies using pip:
  - pip install -r requirements.txt


# Usage

- Setting Chrome WebDriver Path in launch.json

    Before running the scraping scripts, we need to specify the path to the Chrome WebDriver in the VSCode launch.json file. 
    This step is essential to ensure that the Selenium library can access the WebDriver when executing the scraping scripts.

    - Open your project in Visual Studio Code (VSCode)
    - In launch.json file in "Python : Web Scraper" configuration
    - Set "CHROME_DRIVER_PATH" to your chrome driver path

- Run the script

    - In VSCode
        - In the left sidebar, click on the "Run and Debug" icon.
        - From here Run the "Python : Web Scraper" configuration

-   View the results:
    Once the scraping process is completed, the script will save the extracted data in a folder named scraped_data in the same directory.
    Open the product_data.json file to view the scraped product data.
    Open the reivews.json file to view the scraped product data.


- [ Optional ]


#---------------------------------------------------------------------------------------------

    - Setting up the proxy server [ ONLY IF VPN CONNECTION IS NOT PRESENT ]

        - In launch.json file in "Python : Web Scraper" configuration
        - Set "PROXY_SERVER_IP_PORT" to your proxy server ip address and port
            -  PROXY_SERVER_IP_PORT: {proxy_server_ip_address}:{proxy_server_port} 

        - Now scraper_initiator.py file
            - In "__init__" function, uncomment this part of code
                # proxy_ip_port = os.environ["PROXY_SERVER_IP_PORT"]
                # self.options.add_argument(f'--proxy-server={proxy_ip_port}')

#---------------------------------------------------------------------------------------------

    - Enabling Web Page Translation [ For compaitable chrome version ]

        - In product_scraper.py file
            - In "__init__" function, uncomment this part of code
            # options.add_argument('--lang=en')
            # prefs = {
            #     "translate_whitelists": {"fr": "en"},
            #     "translate": {"enabled": "true"}
            # }
            # options.add_experimental_option("prefs", prefs)


        - In review_scraper.py file
            - In "__init__" function, uncomment this part of code
            # options.add_argument('--lang=en')
            # prefs = {
            #     "translate_whitelists": {"cs": "en"},
            #     "translate": {"enabled": "true"}
            # }
            # options.add_experimental_option("prefs", prefs)

#---------------------------------------------------------------------------------------------

# Disclaimer

- You would require vpn connected to run the webscraping solution ( Vpn Connection Preferably : european region )
- If you don't have VPN on the system you can run the solution by setting up the proxy server, follow steps included in usage section [ Setting up the proxy server ]
- If you have compaitable chrome version for webpage translation, follow setps include in usage section [ Enabling Webpage translation ]

