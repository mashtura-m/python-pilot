import re

import pandas as pd
from selenium.webdriver.common.by import By

from utils.seleniumEngine import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_row_data(rows):
    """Extract data from table rows."""
    data = []
    for row in rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
            sanction_type = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            nationality = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
            data.append({"Name": name, "SanctionType": sanction_type, "Nationality": nationality})
        except Exception as e:
            logger.warning(f"Failed to extract row data: {e}")
            continue
    return data


def parse_pagination_text(page_text):
    logger.info(page_text)
    match = re.search(r'of\s+(\d+)', page_text)
    if match:
        return int(match.group(1))
    return None


def initParsing():
    """Main scraping function."""
    main_url = 'https://sanctions.adb.org/sanctions/published'
    driver = None

    try:
        driver = create_webdriver()
        driver.get(main_url)

        # Wait for page to load properly
        # wait_for_element(driver, (By.CLASS_NAME, 'gap-xl'), 20, EC.visibility_of_element_located)
        time.sleep(10)
        logger.info("Page loaded successfully.")

        # Scroll and get pagination info
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_element = wait_for_element(driver, (By.CLASS_NAME, 'gap-xl'), 20, EC.visibility_of_element_located)

        total_pages = parse_pagination_text(page_element.text)
        logger.info(f"Found {total_pages} total pages")

        all_data = []
        page_count = 1
        max_pages = 5

        while page_count <= min(max_pages, total_pages or max_pages):
            logger.info(f"Scraping page {page_count}")

            # Wait for table rows to load
            rows = wait_for_element(driver, (By.CSS_SELECTOR, 'table tbody tr'), 10,
                                    EC.presence_of_all_elements_located)

            page_data = extract_row_data(rows)
            all_data.extend(page_data)
            logger.info(f"All Data {all_data}")
            break
            if page_count != 1:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait_and_click(driver, (By.XPATH, "//button[./svg/path[contains(@d, 'M6.1584')]]"))
            # //*[@id="__next"]/main/div/div[2]/div[2]/div[2]/div/button[3]
            page_count += 1

        df = pd.DataFrame(all_data)
        logger.info(f"Scraped {len(df)} total records")
        return df

    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise
    finally:
        if driver:
            tear_down(driver)


if __name__ == "__main__":
    output_df = initParsing()
    logger.info(output_df.head())
