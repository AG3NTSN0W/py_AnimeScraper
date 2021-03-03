import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

import time


class Selenium:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--incognito')
        options.add_argument('--log-level=OFF')
        print(chrome_ip)
        self.driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub", options=options)
    pass

    def loadPage(self, url):
        try:
            self.driver.get(url)
            return self.driver.page_source
        finally:
            self.driver.quit()
            pass
        return None

    def loadPageAndWaitForElement(self, url, elementId, delay=0):
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, delay)
            wait.until(EC.element_to_be_clickable((By.ID, elementId)))
            return self.driver.page_source
        except TimeoutException:
            return None
        finally:
            self.driver.quit()
            pass
        return None

    def loadPageAndWait(self, url, delay=0):
        try:
            self.driver.get(url)
            time.sleep(delay)
            return self.driver.page_source
        finally:
            self.driver.quit()
            pass
        return None


pass
