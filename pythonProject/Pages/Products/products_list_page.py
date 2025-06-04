from playwright.sync_api import Page, Locator, expect
from Pages.base_page import BasePage


class ProductsListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._selectors = self._Selectors()

    def sort_products_by(self, sort_value: str):
        """
        Selects a sorting option by its value.
        :param sort_value: One of 'az', 'za', 'lohi', 'hilo'
        """
        self.current_page.locator("[data-test='product-sort-container']").select_option(sort_value)

    def get_all_product_titles(self):
        """
        Returns a list of all visible product titles on the inventory page.
        """
        return self.current_page.locator(".inventory_item_name").all_inner_texts()


    def add_product_to_cart(self, product_name: str):
        self.current_page.click(self._selectors.add_to_cart_button(product_name))

    def verify_add_button_for_product(self, product_name: str):
        """
        Verifies that the 'Add to cart' button is visible for a specific product.
        """
        item = self.current_page.locator(".inventory_item").filter(has_text=product_name)
        add_btn = item.locator("button")
        expect(add_btn).to_have_text("Add to cart")

    def get_remove_button_locator(self, product_name: str) -> Locator:
        return self.current_page.locator(self._selectors.remove_from_cart_button(product_name))

    def remove_product_from_cart(self, product_name: str):
        self.current_page.click(self._selectors.remove_from_cart_button(product_name))


    def get_cart_icon_locator(self) -> Locator:
        return self.current_page.locator(self._selectors.CART_ICON)

    def click_burger_menu(self):
        self.current_page.click(self._selectors.BURGER_MENU_BUTTON)

    def click_logout(self):
        self.current_page.click(self._selectors.LOGOUT_BUTTON)
        from Pages.Login.login_page import LoginPage
        return LoginPage(self.current_page)


    class _Selectors:
        PRODUCTS = "[data-test='inventory-item']"
        CART_ICON = "[data-test='shopping-cart-link']"
        BURGER_MENU_BUTTON = "#react-burger-menu-btn"
        LOGOUT_BUTTON = "#logout_sidebar_link"

        @staticmethod
        def add_to_cart_button(product_name: str) -> str:
            return f"{ProductsListPage._Selectors.PRODUCTS}:has-text('{product_name}') .pricebar button:text('Add to cart')"

        @staticmethod
        def remove_from_cart_button(product_name: str) -> str:
            return f"{ProductsListPage._Selectors.PRODUCTS}:has-text('{product_name}') .pricebar button:text('Remove')"
