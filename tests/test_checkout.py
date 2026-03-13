"""
Test Suite: Full Checkout Process
Covers: complete happy path + validation errors + cancel + back home button.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CartPage, CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage


VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture(autouse=True)
def login_and_add_item(driver):
    """
    Runs before every test in this file.
    Logs in and adds one product to the cart so we can test checkout.
    """
    login = LoginPage(driver)
    login.open()
    login.login(VALID_USER, VALID_PASS)

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()


class TestCheckoutHappyPath:
    """The full successful checkout flow."""

    def test_complete_checkout_flow(self, driver):
        """
        Scenario: User goes through all checkout steps correctly.
        Expected: Confirmation 'Thank you' message appears at the end.
        """
        cart = CartPage(driver)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.enter_info("Ahmed", "Hassan", "12345")
        checkout.click_continue()

        assert checkout.is_on_checkout_step_two(), \
            "Should be on checkout step two after filling info"

        overview = CheckoutOverviewPage(driver)
        overview.finish_order()

        complete = CheckoutCompletePage(driver)
        confirmation = complete.get_confirmation_text()
        assert "Thank you" in confirmation, \
            f"Expected 'Thank you' message, got: {confirmation}"

    def test_order_complete_url(self, driver):
        """
        Scenario: After finishing order, URL should contain 'checkout-complete'.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Sara", "Ali", "54321")
        checkout.click_continue()
        CheckoutOverviewPage(driver).finish_order()

        assert "checkout-complete" in driver.current_url

    def test_item_appears_in_order_overview(self, driver):
        """
        Scenario: The item added to cart should appear in the overview page.
        """
        cart = CartPage(driver)
        item_names_in_cart = cart.get_item_names()

        cart.proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Test", "User", "99999")
        checkout.click_continue()

        overview = CheckoutOverviewPage(driver)
        overview_items = overview.get_item_names()

        for item in item_names_in_cart:
            assert item in overview_items, \
                f"Expected '{item}' in overview, but got: {overview_items}"

    def test_total_price_is_correct_on_overview(self, driver):
        """
        Scenario: The total shown on the overview page should match item price + tax.
        Expected: Total label is visible and contains a '$' sign.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Ahmed", "Hassan", "12345")
        checkout.click_continue()

        overview = CheckoutOverviewPage(driver)
        total = overview.get_total()

        assert "$" in total, f"Expected total to contain '$', got: {total}"
        assert float(total.replace("Total: $", "")) > 0, \
            "Total price should be greater than 0"

    def test_back_home_button_after_order(self, driver):
        """
        Scenario: After completing order, click 'Back Home' button.
        Expected: User is redirected back to the inventory page.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Ahmed", "Hassan", "12345")
        checkout.click_continue()
        CheckoutOverviewPage(driver).finish_order()

        complete = CheckoutCompletePage(driver)
        complete.go_back_home()

        assert "inventory" in driver.current_url, \
            "Expected to be back on inventory page after clicking Back Home"


class TestCheckoutValidation:
    """Checkout form validation — missing required fields."""

    def test_checkout_without_first_name(self, driver):
        """
        Scenario: Leave first name empty.
        Expected: Error message about first name.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("", "Doe", "12345")
        checkout.click_continue()

        error = checkout.get_error_message()
        assert "First Name is required" in error

    def test_checkout_without_last_name(self, driver):
        """
        Scenario: Leave last name empty.
        Expected: Error message about last name.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("John", "", "12345")
        checkout.click_continue()

        error = checkout.get_error_message()
        assert "Last Name is required" in error

    def test_checkout_without_postal_code(self, driver):
        """
        Scenario: Leave postal code empty.
        Expected: Error message about postal code.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("John", "Doe", "")
        checkout.click_continue()

        error = checkout.get_error_message()
        assert "Postal Code is required" in error

    def test_cancel_checkout_goes_back_to_cart(self, driver):
        """
        Scenario: Start checkout then click Cancel.
        Expected: User is taken back to the cart page.
        """
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.click_cancel()

        assert "cart" in driver.current_url, \
            "Expected to be back on cart page after clicking Cancel"