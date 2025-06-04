import pytest
from Pages.Products.products_list_page import ProductsListPage
from Utilities.product_data_reader import ProductDataReader
from Tests.test_base import BaseTest
from playwright.sync_api import expect

@pytest.mark.usefixtures("setup_with_login")
class TestProductList(BaseTest):

    @classmethod
    def setup_class(cls):
        # Load product list once for all tests
        cls.products = ProductDataReader.get_products_to_add()

    def test_cart_flow_all_products(self):
        """
        Add all products to cart, verify they appear in cart with 'Remove' button,
        then remove all products and verify 'Add to cart' is visible again.
        """
        self.logger.info("Starting test_cart_flow_all_products")
        self.products_page = ProductsListPage(self.page)

        # Add all products to cart and verify 'Remove' buttons
        self.logger.info("Adding all products to cart")
        for product in self.products:
            self.products_page.add_product_to_cart(product)
            remove_btn = self.products_page.get_remove_button_locator(product)
            expect(remove_btn).to_be_visible()

        # Navigate to cart and verify all products appear
        self.logger.info("Navigating to cart and verifying all products are listed")
        self.products_page.get_cart_icon_locator().click()
        for product in self.products:
            cart_item = self.page.locator(".cart_item").locator(".inventory_item_name", has_text=product)
            expect(cart_item).to_be_visible()

        # Return to products page
        self.page.go_back()

        # Remove all products from cart and verify 'Add to cart' button
        self.logger.info("Removing all products and verifying 'Add to cart' buttons")
        for product in self.products:
            self.products_page.remove_product_from_cart(product)
            self.products_page.verify_add_button_for_product(product)

        self.logger.info("Completed test_cart_flow_all_products")

    def test_sort_by_name_descending(self):
        """
        Sort products by Name (Z to A) and validate that the order is correct.
        """
        self.logger.info("Starting test_sort_by_name_descending")
        self.products_page = ProductsListPage(self.page)

        # Perform sorting action
        self.logger.info("Sorting products by name (Z to A)")
        self.products_page.sort_products_by("za")

        # Verify number of rendered items matches expected product count
        expect(self.page.locator(".inventory_item_name")).to_have_count(len(self.products))

        # Get all product titles as shown on the UI
        product_names = self.products_page.get_all_product_titles()

        # Validate sorting order
        expected_order = sorted(self.products, reverse=True)
        assert product_names == expected_order, f"Expected: {expected_order} | Got: {product_names}"

        self.logger.info("Completed test_sort_by_name_descending")




