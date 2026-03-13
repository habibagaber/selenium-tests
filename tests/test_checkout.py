import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CartPage, CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture(autouse=True)
def login_and_add_item(driver):
    login = LoginPage(driver)
    login.open()
    login.login(VALID_USER, VALID_PASS)
    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()  # ✅ navigate to cart page before tests start


class TestCheckoutHappyPath:

    def test_complete_checkout_flow(self, driver):
        cart = CartPage(driver)
        cart.proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Ahmed", "Hassan", "12345")
        checkout.click_continue()
        assert checkout.is_on_checkout_step_two()
        overview = CheckoutOverviewPage(driver)
        overview.finish_order()
        complete = CheckoutCompletePage(driver)
        confirmation = complete.get_confirmation_text()
        assert "Thank you" in confirmation

    def test_order_complete_url(self, driver):
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("Sara", "Ali", "54321")
        checkout.click_continue()
        CheckoutOverviewPage(driver).finish_order()
        assert "checkout-complete" in driver.current_url

    def test_item_appears_in_order_overview(self, driver):
        # ✅ Fix: read item names NOW (we are already on cart page)
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


class TestCheckoutValidation:

    def test_checkout_without_first_name(self, driver):
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("", "Doe", "12345")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "First Name is required" in error

    def test_checkout_without_last_name(self, driver):
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("John", "", "12345")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "Last Name is required" in error

    def test_checkout_without_postal_code(self, driver):
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.enter_info("John", "Doe", "")
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "Postal Code is required" in error