import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Parser:
    def __init__(self):
        self._init_webdriver()

    def _init_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('enable-features=NetworkServiceInProcess')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
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

    def get_from_url(self, url: str) -> (str, str):
        # try:
            if self.driver.current_url == url:
                self.driver.refresh()
            else:
                self.driver.get(url)

            row_class_name = 'ant-table-row'
            # _ = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, row_class_name)))
            # _ = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.ID, 'rc-tabs-0-tab-splTransfers')))
            sleep(10)
            self.driver.save_screenshot('screen.jpg')
            _ = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, 'ant-table-tbody')))

            self.driver.save_screenshot('screen2.jpg')
            # row_objs = self.driver.find_elements(By.CLASS_NAME, value=row_class_name)
            # last_row_obj = row_objs[0]

            tables = self.driver.find_elements(By.CLASS_NAME, value='ant-table-tbody')
            spl_table = tables[1]
            last_row_obj = spl_table.find_element(By.CLASS_NAME, value=row_class_name)
            last_row_href = last_row_obj.find_element(By.TAG_NAME, value='a').get_attribute('href')
            last_row_cells = last_row_obj.find_elements(By.CLASS_NAME, 'ant-table-cell')
            amount_cell = last_row_cells[-1]
            amount_text = amount_cell.text.replace('\n', '')

            return last_row_href, amount_text
        # except Exception as e:
        #     logger.fatal(f'Cant parse {url}: {e} - {e.__class__.__name__}')

    @staticmethod
    def stub_get_from_url(url: str):
        return random.randint(1, 10)


if __name__ == '__main__':
    parser = Parser()
    print(parser.get_from_url('https://solscan.io/account/BQJoDFBsvETyRjPvtLoRu6wzNiwz7SScXL8ZLpjm8sfZ#splTransfers'))
