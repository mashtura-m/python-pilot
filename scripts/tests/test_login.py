import pytest
from selenium.webdriver.common.by import By

from pages.login_page import Login_page
from utils.seleniumEngine import create_webdriver


@pytest.fixture
def set_up():
    driver = create_webdriver()
    driver.get("https://www.saucedemo.com/")
    login = Login_page(driver, (By.ID, "user-name"), (By.ID, "password"), (By.ID, "login-button"))
    return driver, login


def test_valid_login(set_up):
    (driver, login) = set_up
    login.do_login("standard_user", "secret_sauce")
    test_title = "Swag Labs"
    assert driver.title == test_title, "Login Successful"


def test_invalid_login(set_up):
    (driver, login) = set_up
    login.do_login("anika", "secret_sauce")
    error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']")
    assert error_message is not None, "Login Invalid"
