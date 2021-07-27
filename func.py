from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time

SENT_BUTTON = 'button._4sWnG'
ALERT_BUTTON = 'div._2QSxG._2vB9T'
MAIN_PAGE = '._3Nsgw'
SPINNER = 'div.PWkc7 ._3dpR7'


# Function to send text and handle invalid number popups
def interact(browser, selector):
    try:
        button = WebDriverWait(browser, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        time.sleep(1)
        button.click()
        return selector
    except:
        return


# Function to automate the entire process for each number
def automate(browser, url, delay):

    # Make sure everything finished loading before moving on to the next number
    while True:
        try:
            browser.find_element_by_css_selector(SPINNER)
        except:
            try:
                browser.get(url)
                WebDriverWait(browser, 15).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, MAIN_PAGE)))
                break
            except:
                time.sleep(1)

    # Send text and handle invalid number popups concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(delay):
            tasks = [executor.submit(interact, browser, SENT_BUTTON),
                     executor.submit(interact, browser, ALERT_BUTTON)]
            for task in concurrent.futures.as_completed(tasks):
                result = task.result()
                if result:
                    return result
