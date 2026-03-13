"""
Test Suite: Cart — Adding and Removing Items
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CartPage


VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture(autouse=True)
def login_first(driver):
    """
    This fixture runs automatically before every test in this file.
    It logs in so tests start on the inventory page.
    """
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(VALID_USER, VALID_PASS)
    assert login_page.is_logged_in(), "Login failed during test setup"


class TestAddToCart:
    """Tests for adding items to the cart."""

    def test_add_one_item_updates_cart_badge(self, driver):
        """
        Scenario: Add one item.
        Expected: Cart badge shows '1'.
        """
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()

        count = inventory.get_cart_item_count()
        assert count == 1, f"Expected cart count 1, got {count}"

    def test_add_multiple_items_updates_badge(self, driver):
        """
        Scenario: Add two items one after another.
        Expected: Cart badge shows '2'.
        """
        inventory = InventoryPage(driver)
        inventory.add_item_by_index(0)
        inventory.add_item_by_index(1)

        count = inventory.get_cart_item_count()
        assert count == 2, f"Expected cart count 2, got {count}"

    def test_added_item_appears_in_cart(self, driver):
        """
        Scenario: Add first item, then go to cart.
        Expected: That item is visible in the cart.
        """
        inventory = InventoryPage(driver)
        # Get the name of the first product
        product_names = inventory.get_product_names()
        first_product = product_names[0]

        inventory.add_first_item_to_cart()
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart_items = cart.get_item_names()
        assert first_product in cart_items, \
            f"Expected '{first_product}' in cart, but found: {cart_items}"


class TestRemoveFromCart:
    """Tests for removing items from the cart."""

    def test_remove_item_from_inventory_page(self, driver):
        """
        Scenario: Add item, then remove it directly from inventory page.
        Expected: Cart badge disappears (count = 0).
        """
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

        cart = CartPage(driver)
        assert cart.get_item_count() == 1

        cart.remove_item(index=0)
        assert cart.is_empty(), "Cart should be empty after removing the only item"

    def test_cart_badge_disappears_after_removal(self, driver):
        """
        Scenario: Add then remove item.
        Expected: Badge is no longer shown (count returns 0).
        """
        inventory = InventoryPage(driver)
        inventory.add_first_item_to_cart()
        inventory.remove_first_item_from_cart()

        count = inventory.get_cart_item_count()
        assert count == 0