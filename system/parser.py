import random
from time import sleep
from typing import Union, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from system.cookies import load_cookies
from system.logs import logger


class Parser:
    def __init__(self):
        self._init_webdriver()
        # self._load_cookies()
        self._login()

    def _init_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('enable-features=NetworkServiceInProcess')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument('headless')

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

    def _load_cookies(self) -> None:
        """
        Загрузка cookies из файла в driver
        :return: None
        """

        cookies_list = load_cookies()
        self.driver.get('https://solscan.io/')
        for cookie in cookies_list:
            print(cookie)
            if cookie['domain'] == '.solscan.io':
                self.driver.add_cookie(cookie)

    def _login(self) -> None:
        self.driver.get('https://solscan.io/user/signin')
        _ = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.ID, 'email')))
        login_field = self.driver.find_element(By.ID, value='email')
        login_field.send_keys('tkvitko@gmail.com')
        password_field = self.driver.find_element(By.ID, value='password')
        password_field.send_keys('L42&#q8mX&J&br$')
        button_submit = self.driver.find_element(By.CLASS_NAME, value='ant-btn')
        button_submit.click()

    def get_from_url(self, url: str) -> Union[List | None]:
        try:
            if self.driver.current_url == url:
                self.driver.refresh()
            else:
                self.driver.get(url)

            row_class_name = 'ant-table-row'
            _ = WebDriverWait(self.driver, 90).until(ec.presence_of_element_located((By.CLASS_NAME, 'ant-table-tbody')))
            sleep(10)
            self.driver.save_screenshot('screen.png')
            tables = self.driver.find_elements(By.CLASS_NAME, value='ant-table-tbody')
            try:
                spl_table = tables[1]  # if len(tables) > 1 else tables[0]
            except IndexError:
                return None

            rows = []
            row_objs = spl_table.find_elements(By.CLASS_NAME, value=row_class_name)
            for row_obj in row_objs:
                row_href = row_obj.find_element(By.TAG_NAME, value='a').get_attribute('href')
                row_cells = row_obj.find_elements(By.CLASS_NAME, 'ant-table-cell')
                amount_cell = row_cells[-1]
                amount_text = amount_cell.text.replace('\n', '')
                rows.append((row_href, amount_text))

            return rows

            # last_row_obj = spl_table.find_element(By.CLASS_NAME, value=row_class_name)
            # last_row_href = last_row_obj.find_element(By.TAG_NAME, value='a').get_attribute('href')
            # last_row_cells = last_row_obj.find_elements(By.CLASS_NAME, 'ant-table-cell')
            # amount_cell = last_row_cells[-1]
            # amount_text = amount_cell.text.replace('\n', '')
            #
            # return last_row_href, amount_text
        except Exception as e:
            logger.fatal(f'Cant parse {url}: {e} - {e.__class__.__name__}')

    @staticmethod
    def stub_get_from_url(url: str):
        return random.randint(1, 10)


if __name__ == '__main__':
    parser = Parser()
    print(parser.get_from_url('https://solscan.io/account/BQJoDFBsvETyRjPvtLoRu6wzNiwz7SScXL8ZLpjm8sfZ#splTransfers'))
