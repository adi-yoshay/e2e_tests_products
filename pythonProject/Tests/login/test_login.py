from Tests.test_base import BaseTest
import pytest
from Pages.Login.login_page import LoginPage
from Utilities.user_data_reader import UserDataReader
from playwright.sync_api import expect

@pytest.mark.usefixtures("setup_browser_context")
class TestLogin(BaseTest):

    @pytest.mark.parametrize(
        "user_type, expected_result",
        [
            ("Valid", "Products"),
            ("Invalid", "Epic sadface: Username and password do not match any user in this service"),
            ("Locked", "Epic sadface: Sorry, this user has been locked out.")
        ]
    )
    def test_login_various_credentials(self, user_type, expected_result):
        self.logger.info(f"Starting login test for user type: '{user_type}'")

        # Get credentials from test data
        creds = UserDataReader.get_user_credentials(user_type)
        login_page = LoginPage(self.page)

        # Perform login
        self.logger.info("Attempting to log in...")
        login_page.login_to_application(creds["username"], creds["password"])

        # Validate outcome based on expected result
        if user_type == "Valid":
            self.logger.info("Verifying successful login...")
            expect(login_page.screen_title()).to_have_text(expected_result)
        else:
            self.logger.info(f"Verifying error message for user: {user_type}")
            expect(login_page.get_error_locator()).to_have_text(expected_result)

        # Log test end
        self.logger.info(f"Login test passed for user type: '{user_type}'")

