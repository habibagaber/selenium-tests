from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")  # ✅ new

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)

    def get_cart_items(self):
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_item_count(self):
        return len(self.get_cart_items())

    def get_item_names(self):
        self.wait.until(EC.url_contains("cart"))
        self.wait.until(EC.presence_of_element_located(self.ITEM_NAMES))
        names = self.driver.find_elements(*self.ITEM_NAMES)
        return [n.text for n in names]

    def get_item_prices(self):  # ✅ new
        """Return list of item prices as floats e.g. [9.99]."""
        prices = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(p.text.replace("$", "")) for p in prices]

    def remove_item(self, index=0):
        buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
        buttons[index].click()

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()

    def is_empty(self):
        return self.get_item_count() == 0


class CheckoutPage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.XPATH, "//*[@data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def enter_info(self, first_name, last_name, postal_code):
        self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        ).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def click_cancel(self):  # ✅ new
        """Click Cancel to go back to the cart."""
        self.wait.until(EC.element_to_be_clickable(self.CANCEL_BUTTON)).click()

    def get_error_message(self):
        self.wait.until(EC.url_contains("checkout-step-one"))
        error = self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return error.text

    def is_on_checkout_step_two(self):
        return "checkout-step-two" in self.driver.current_url


class CheckoutOverviewPage:
    FINISH_BUTTON = (By.ID, "finish")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    CANCEL_BUTTON = (By.ID, "cancel")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_item_names(self):
        self.wait.until(EC.presence_of_element_located(self.ITEM_NAMES))
        items = self.driver.find_elements(*self.ITEM_NAMES)
        return [i.text for i in items]

    def get_total(self):
        """Return the total price string e.g. 'Total: $32.39'."""
        return self.wait.until(
            EC.visibility_of_element_located(self.TOTAL_LABEL)
        ).text

    def finish_order(self):
        self.wait.until(EC.url_contains("checkout-step-two"))
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON)).click()

    def is_order_complete(self):
        return "checkout-complete" in self.driver.current_url


class CheckoutCompletePage:
    CONFIRMATION_HEADER = (By.XPATH, "//*[contains(@class,'complete-header')]")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_confirmation_text(self):
        self.wait.until(EC.url_contains("checkout-complete"))
        header = self.wait.until(
            EC.visibility_of_element_located(self.CONFIRMATION_HEADER)
        )
        return header.text

    def go_back_home(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BACK_HOME_BUTTON)
        ).click()
        self.wait.until(EC.url_contains("inventory"))