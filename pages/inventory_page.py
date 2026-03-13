from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """
    Page Object Model for the Inventory (Products) Page.
    This is the page you land on after a successful login.
    """

    URL = "https://www.saucedemo.com/inventory.html"

    # --- Locators ---
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Navigate directly to the inventory page."""
        self.driver.get(self.URL)

    def get_all_add_buttons(self):
        """Return all 'Add to cart' buttons on the page."""
        return self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)

    def add_first_item_to_cart(self):
        """Click the first 'Add to cart' button available."""
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTONS)
        )
        buttons[0].click()

    def add_item_by_index(self, index):
        """Add a specific item to the cart by its position (0 = first)."""
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def remove_first_item_from_cart(self):
        """Click the first 'Remove' button (after an item has been added)."""
        remove_btn = self.wait.until(
            EC.element_to_be_clickable(self.REMOVE_BUTTONS)
        )
        remove_btn.click()

    def get_cart_item_count(self):
        """
        Return the number shown on the cart icon badge.
        Returns 0 if the badge is not visible (empty cart).
        """
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        """Click the cart icon to navigate to the cart page."""
        self.driver.find_element(*self.CART_ICON).click()

    def get_product_names(self):
        """Return a list of all product names shown on the page."""
        items = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [item.text for item in items]