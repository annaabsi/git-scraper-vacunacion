import json
import os
import random
import time

import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import datetime

def scraper(PUBLIC_TABLEAU_VIEW,
            TIME_SECONDS_TO_WAIT_UNTIL_DASHBOARD_LOAD,
            SCREENSHOT_FILENAME):
    # Main code taken from https://thinkdiff.net/how-to-run-javascript-in-python-web-scraping-web-testing-16bd04894360
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=600x800")

    # download Chrome Webdriver
    # https://sites.google.com/a/chromium.org/chromedriver/download
    # put driver executable file in the script directory
    chrome_driver = os.path.join(os.getcwd(),  "headers/chromedriver")

    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=chrome_driver)

    driver.get(PUBLIC_TABLEAU_VIEW)

    time.sleep(TIME_SECONDS_TO_WAIT_UNTIL_DASHBOARD_LOAD+random.uniform(0, 1))

    driver.get_screenshot_as_file("resultados/"+SCREENSHOT_FILENAME)

    driver.close()


def img2text(SCREENSHOT_FILENAME):

    img = cv2.imread("resultados/"+SCREENSHOT_FILENAME)

    cut_image = img[30: 150, :]

    cv2.imwrite(
        "resultados/"+SCREENSHOT_FILENAME[:-4]+'_cuted'+SCREENSHOT_FILENAME[-4:], cut_image)

    text = pytesseract.image_to_string(cut_image)

    return text


if name == "main":

    URL_DOSIS1 = 'https://public.tableau.com/views/VacunaCovid_CMP/Dosis1?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Alanguage=en-GB&:embed=y&:showVizHome=n&:apiID=host1#navType=0&navSrc=Parse'
    URL_DOSIS2 = 'https://public.tableau.com/views/VacunaCovid_CMP/Dosis2?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Alanguage=en-GB&:embed=y&:showVizHome=n&:apiID=host1#navType=0&navSrc=Parse'
    SS = 'python-screenshot.png'
    SS_CUTED = 'python-screenshot-cutted.png'

    ############
    # DOSIS 1 y 2
    ############

    scraper(PUBLIC_TABLEAU_VIEW=URL_DOSIS1,
            TIME_SECONDS_TO_WAIT_UNTIL_DASHBOARD_LOAD=5,
            SCREENSHOT_FILENAME='dosis1-'+SS)
    dosis1_text = img2text(SCREENSHOT_FILENAME='dosis1-'+SS)

    scraper(PUBLIC_TABLEAU_VIEW=URL_DOSIS2,
            TIME_SECONDS_TO_WAIT_UNTIL_DASHBOARD_LOAD=5,
            SCREENSHOT_FILENAME='dosis2-'+SS)
    dosis2_text = img2text(SCREENSHOT_FILENAME='dosis2-'+SS)

    dosis1_number = int(dosis1_text.replace(' ', '').replace(',', ''))
    dosis2_number = int(dosis2_text.replace(' ', '').replace(',', ''))
    print(dosis1_number)
    print(dosis2_number)

    ################
    # SAVING TO JSON
    ################
    dosis_dict = {}
    dosis_dict['dosis1'] = dosis1_number
    dosis_dict['dosis2'] = dosis2_number

    print(dosis_dict)

    with open("resultados/ambas_dosis.json", "w") as outfile:
        json.dump(dosis_dict, outfile)

    text_file = open("resultados/last_run.txt", "w")
    n = text_file.write(datetime.datetime.now())
    text_file.close()
