"""
Test Suite: Login Scenarios
Tests both successful logins (positive) and failed logins (negative).
"""

import pytest
from pages.login_page import LoginPage


# ─────────────────────────────────────────────
# VALID credentials for SauceDemo
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
# ─────────────────────────────────────────────


class TestLoginPositive:
    """Tests that SHOULD succeed (valid credentials)."""

    def test_login_with_valid_credentials(self, driver):
        """
        Scenario: User logs in with correct username and password.
        Expected: Redirected to the inventory/products page.
        """
        page = LoginPage(driver)
        page.open()
        page.login(VALID_USER, VALID_PASS)

        assert page.is_logged_in(), "Expected to be on inventory page after valid login"

    def test_login_url_after_success(self, driver):
        """
        Scenario: After login, confirm URL contains 'inventory'.
        """
        page = LoginPage(driver)
        page.open()
        page.login(VALID_USER, VALID_PASS)

        assert "inventory" in driver.current_url


class TestLoginNegative:
    """Tests that SHOULD fail (invalid credentials)."""

    def test_login_with_wrong_password(self, driver):
        """
        Scenario: Correct username but wrong password.
        Expected: Error message appears, user stays on login page.
        """
        page = LoginPage(driver)
        page.open()
        page.login(VALID_USER, "wrong_password")

        error = page.get_error_message()
        assert "Username and password do not match" in error

    def test_login_with_wrong_username(self, driver):
        """
        Scenario: Wrong username, correct password.
        Expected: Error message appears.
        """
        page = LoginPage(driver)
        page.open()
        page.login("wrong_user", VALID_PASS)

        error = page.get_error_message()
        assert "Username and password do not match" in error

    def test_login_with_empty_username(self, driver):
        """
        Scenario: Leave username blank, fill in password.
        Expected: Error message about required username.
        """
        page = LoginPage(driver)
        page.open()
        page.login("", VALID_PASS)

        error = page.get_error_message()
        assert "Username is required" in error

    def test_login_with_empty_password(self, driver):
        """
        Scenario: Fill in username, leave password blank.
        Expected: Error message about required password.
        """
        page = LoginPage(driver)
        page.open()
        page.login(VALID_USER, "")

        error = page.get_error_message()
        assert "Password is required" in error

    def test_login_with_both_fields_empty(self, driver):
        """
        Scenario: Both username and password are left empty.
        Expected: Error message about required username.
        """
        page = LoginPage(driver)
        page.open()
        page.login("", "")

        error = page.get_error_message()
        assert "Username is required" in error

    def test_login_with_locked_out_user(self, driver):
        """
        Scenario: Use the 'locked_out_user' account (blocked by the app).
        Expected: Error message saying the user has been locked out.
        """
        page = LoginPage(driver)
        page.open()
        page.login("locked_out_user", VALID_PASS)

        error = page.get_error_message()
        assert "locked out" in error.lower()