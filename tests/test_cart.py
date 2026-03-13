"""
Test Suite: Cart — Adding and Removing Items
"""

import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CartPage


VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture(autouse=True)
def login_first(driver):
    """
    Runs automatically before every test in this file.
    Logs in so tests start on the inventory page.
    """
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(VALID_USER, VALID_PASS)
    assert login_page.is_logged_in(), "Login failed during test setup"


class TestAddToCart:
    """Tests for adding items to the cart."""

    def test_add_one_item_updates_cart_badge(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()
        count = inventory.get_cart_item_count()
        assert count == 1, f"Expected cart count 1, got {count}"

    def test_add_multiple_items_updates_badge(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_item_by_index(0)
        inventory.add_item_by_index(1)
        count = inventory.get_cart_item_count()
        assert count == 2, f"Expected cart count 2, got {count}"

    def test_added_item_appears_in_cart(self, driver):
        inventory = InventoryPage(driver)
        first_product = inventory.get_first_product_name()
        inventory.add_first_item_to_cart()
        inventory.go_to_cart()
        cart = CartPage(driver)
        cart_items = cart.get_item_names()
        assert first_product in cart_items, \
            f"Expected '{first_product}' in cart, but found: {cart_items}"

    def test_item_name_and_price_correct_in_cart(self, driver):
        inventory = InventoryPage(driver)
        expected_name = inventory.get_first_product_name()
        expected_price = inventory.get_first_product_price()
        inventory.add_first_item_to_cart()
        inventory.go_to_cart()
        cart = CartPage(driver)
        cart_names = cart.get_item_names()
        cart_prices = cart.get_item_prices()
        assert expected_name in cart_names, \
            f"Product name mismatch. Expected '{expected_name}', got {cart_names}"
        assert expected_price in cart_prices, \
            f"Product price mismatch. Expected '{expected_price}', got {cart_prices}"

    def test_add_all_products_to_cart(self, driver):
        inventory = InventoryPage(driver)
        total_added = inventory.add_all_items_to_cart()
        count = inventory.get_cart_item_count()
        assert count == total_added, \
            f"Expected cart count {total_added}, got {count}"
        assert count == 6, f"SauceDemo has 6 products, but cart shows {count}"


class TestRemoveFromCart:
    """Tests for removing items from the cart."""

    def test_remove_item_from_inventory_page(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()
        assert inventory.get_cart_item_count() == 1
        inventory.remove_first_item_from_cart()
        count = inventory.get_cart_item_count()
        assert count == 0, f"Expected cart count 0 after removal, got {count}"

    def test_remove_item_from_cart_page(self, driver):
        """
        Scenario: Add item, navigate to cart, remove item there.
        Expected: Cart becomes empty.
        """
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()
        inventory.go_to_cart()

        wait = WebDriverWait(driver, 15)
        wait.until(EC.url_contains("cart"))
        wait.until(EC.element_to_be_clickable((By.ID, "checkout")))

        cart = CartPage(driver)
        assert cart.get_item_count() == 1

        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-test^='remove']")
        )).click()

        time.sleep(1)
        assert cart.is_empty(), "Cart should be empty after removing the only item"

    def test_cart_badge_disappears_after_removal(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()
        inventory.remove_first_item_from_cart()
        count = inventory.get_cart_item_count()
        assert count == 0