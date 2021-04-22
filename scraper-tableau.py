import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


DEBUG=1 # 0 to dont render image


def scraper():
    # Main code taken from https://thinkdiff.net/how-to-run-javascript-in-python-web-scraping-web-testing-16bd04894360
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")

    # download Chrome Webdriver
    # https://sites.google.com/a/chromium.org/chromedriver/download
    # put driver executable file in the script directory
    chrome_driver = os.path.join(os.getcwd(),  "headers/chromedriver")

    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)

    driver.get("https://public.tableau.com/profile/aldo.balta#!/vizhome/VacunaCovid_CMP/Dosis1")

    time.sleep(10+random.uniform(0, 1))

    # screenshot capture
    if DEBUG == 1: driver.get_screenshot_as_file("python-scrap.png")

    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div/div[12]/div/div[1]/div[2]/canvas[2]') # Botón congresales

    html=driver.page_source

    driver.close()

scraper()
