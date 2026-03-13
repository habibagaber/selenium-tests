from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Page Object Model (POM) for the Login Page.

    What is POM? Instead of writing browser actions directly in tests,
    we collect all actions for a specific page here. This keeps tests clean
    and makes it easy to update if the website changes.
    """

    URL = "https://www.saucedemo.com"

    # --- Locators (how Selenium finds elements on the page) ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Navigate to the login page."""
        self.driver.get(self.URL)

    def enter_username(self, username):
        """Type into the username field."""
        field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        """Type into the password field."""
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)

    def click_login(self):
        """Click the Login button."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        """Full login action: fill username + password + click login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Return the error message text shown after a failed login."""
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error.text

    def is_logged_in(self):
        """Check if login was successful by verifying the URL changed."""
        return "inventory" in self.driver.current_url