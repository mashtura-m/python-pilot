import json
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_webdriver():
    # Initialize ChromeOptions to set browser preferences
    CHROME_PATH = "/home/user/Documents/Automation/python-pilot-mode/chromedriver"
    service = Service(CHROME_PATH)
    options = Options()
    options.add_argument("--disable-extensions")  # Disable browser extensions
    # options.add_argument("--headless")  # Uncomment this line to run in headless mode (no UI)

    # Example: Adding custom preferences (can be expanded)
    prefs = {"download.default_directory": "/home/user/Documents/Automation/python-pilot-mode/output/reports/"}
    options.add_experimental_option("prefs", prefs)

    # You can also set the user agent or other preferences
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver


def wait_for_element(driver, locator, timeout,condition):
    """Wait for an element to meet the given condition"""
    try:
        element = WebDriverWait(driver, timeout).until(condition(locator))
        logging.debug(f"Element located: {locator}")
        return element
    except Exception as e:
        logging.error(f"Timeout or error occurred while waiting for element: {locator}, error: {str(e)}")
        capture_page_source(driver)
        raise


# Wait and Click function
def wait_and_click(driver,locator):
    """Wait for element to be clickable and click"""
    element = wait_for_element(driver,locator,20, EC.element_to_be_clickable)
    element.click()
    logging.debug(f"Clicked on element: {locator}")
    return element


# Wait and Type function (ideal for inputs)
def wait_and_type(locator, text):
    """Wait for element, type text"""
    element = wait_for_element(locator)
    element.clear()  # Clear field before typing
    element.send_keys(text)
    logging.debug(f"Typed '{text}' into element: {locator}")
    return element


# Re-find element after page state transition
def refind_element(driver, locator):
    """Re-locate element after page refresh or state change"""
    return driver.find_element(*locator)


# Debugging helper function: Capture page source and screenshot
def capture_page_source(driver, error_type="generic"):
    """Capture page source and screenshot for debugging"""
    timestamp = int(time.time())
    page_source = driver.page_source
    page_source_filename = f"page_source_{error_type}_{timestamp}.html"
    screenshot_filename = f"screenshot_{error_type}_{timestamp}.png"

    # Save page source to file
    with open(page_source_filename, "w") as file:
        file.write(page_source)

    # Capture screenshot
    driver.save_screenshot(screenshot_filename)
    logging.debug(f"Captured page source and screenshot for error: {error_type}")


# Function to save cookies
def save_cookies(driver, filename):
    cookies = driver.get_cookies()  # Get all cookies
    with open(filename, "w") as file:
        json.dump(cookies, file)  # Save cookies in JSON format
    print(f"Cookies saved to {filename}.")


# Function to load cookies
def load_cookies(driver):
    filename = "/home/user/Documents/Automation/python-pilot-mode/data/cookies.json"
    try:
        # Load cookies from the JSON file
        with open(filename, "r") as file:
            cookies = json.load(file)

        # Add each cookie to the browser
        for cookie in cookies:
            driver.add_cookie(cookie)

        print("Cookies loaded successfully.")
        return True
    except Exception:
        print(f"Cookie file '{filename}' not found.")
        # If cookies are not found, save the cookies (you could decide to save after login instead)
        save_cookies(driver, filename)
