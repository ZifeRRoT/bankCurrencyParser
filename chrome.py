from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def run_browser(url):
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get(url)
    page = driver.page_source
    driver.quit()
    return page
