from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from system.logs import logger


class Parser:
    def __init__(self):
        self._init_webdriver()

    def _init_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('enable-features=NetworkServiceInProcess')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('headless')

        max_attempts = 5
        timeout = 60
        attempt = 0
        driver_loaded = False

        while not driver_loaded and attempt < max_attempts:
            try:
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                               options=chrome_options)
                driver_loaded = True
            except Exception as e:
                print(e)
                attempt += 1
                sleep(timeout)

    def get_from_url(self, url: str):
        try:
            self.driver.get(url)
            row_class_name = 'ant-table-row'
            _ = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, row_class_name)))
            last_row_obj = self.driver.find_element(By.CLASS_NAME, value=row_class_name)
            last_row_href = last_row_obj.find_element(By.TAG_NAME, value='a').get_attribute('href')
            return last_row_href
        except Exception as e:
            logger.fatal(f'Cant parse {url}: {e} - {e.__class__.__name__}')


if __name__ == '__main__':
    parser = Parser()
    print(parser.get_from_url('https://solscan.io/account/BQJoDFBsvETyRjPvtLoRu6wzNiwz7SScXL8ZLpjm8sfZ#splTransfers'))

