import pytest
from Pages.Login.login_page import LoginPage
from Pages.Products.products_list_page import ProductsListPage
from Utilities.read_config import AppConfiguration
from Tests.test_base import BaseTest
from playwright.sync_api import expect

@pytest.mark.usefixtures("setup_with_login")
class TestLogout(BaseTest):

    def test_logout(self):
        """
        Verify that a user can log out successfully.
        """

        # Step 1: Initialize Products page object (already logged in via fixture)
        self.product_page = ProductsListPage(self.page)

        # Step 2: Click burger menu and log out
        self.product_page.click_burger_menu()
        login_page = self.product_page.click_logout()

        # Step 3: Verify login button is visible
        expect(login_page.get_login_button_locator()).to_be_visible()

        # Step 4: Verify redirected to login page URL
        config = AppConfiguration.get_common_info()
        expect(login_page.current_page).to_have_url(config["Url"])
        self.logger.info("Test finished: Logout successful and login page loaded")


