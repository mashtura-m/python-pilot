from utils.seleniumEngine import *


class Login_page:

    def __init__(self, driver, username_locator, password_locator, login_button_locator):
        """
Initializes the LoginPage with dynamic locators and valid page title.
:param driver: WebDriver instance
:param username_locator: Locator tuple for username field
:param password_locator: Locator tuple for password field
:param login_button_locator: Locator tuple for login button
"""
        self.driver = driver
        self.username_locator = username_locator
        self.password_locator = password_locator
        self.login_button_locator = login_button_locator

    def do_login(self, username, password):
        time.sleep(10)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def enter_username(self, username):
        username_handle = wait_for_element(self.driver,self.username_locator, 10, EC.visibility_of_element_located)
        username_handle.send_keys(username)
        pass

    def enter_password(self, password):
        username_handle = wait_for_element(self.driver,self.password_locator, 10, EC.visibility_of_element_located)
        username_handle.send_keys(password)
        pass

    def click_login(self):
        wait_and_click(self.driver, self.login_button_locator)
        pass
