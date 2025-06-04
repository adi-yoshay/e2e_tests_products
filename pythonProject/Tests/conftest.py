
import base64
import pytest
from playwright.sync_api import sync_playwright
from Pages.Login.login_page import LoginPage
from Utilities.read_config import AppConfiguration
import os
from datetime import datetime


# =======================
# Shared Setup Utilities
# =======================

def get_browser(browser_name, playwright, launch_options):
    if browser_name == "chromium":
        return playwright.chromium.launch(**launch_options, args=['--start-maximized'])
    elif browser_name == "firefox":
        return playwright.firefox.launch(**launch_options)


# ================================
# Function-scoped setup (no login)
# For login tests only
# ================================
@pytest.fixture(scope="function")
def setup_browser_context(request):
    config = AppConfiguration.get_app_configuration()
    common = AppConfiguration.get_common_info()

    playwright = sync_playwright().start()

    browser_name = request.config.getoption("--browser-name")
    browser = get_browser(
        browser_name,
        playwright,
        launch_options={
            "headless": eval(config["Headless"]),
            "slow_mo": float(config["SlowMo"])
        }
    )

    context = browser.new_context(
        base_url=common["Url"],
        no_viewport=True
    )
    context.set_default_navigation_timeout(float(config["DefaultNavigationTimeout"]))
    context.set_default_timeout(float(config["DefaultTimeout"]))

    page = context.new_page()
    page.goto(common["Url"])

    request.cls.page = page
    yield
    page.close()
    browser.close()
    playwright.stop()

# ====================================
# Class-scoped setup + login included
# For all other tests
# ====================================
@pytest.fixture(scope="class")
def setup_with_login(request):
    config = AppConfiguration.get_app_configuration()
    common = AppConfiguration.get_common_info()

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=eval(config["Headless"]),
        slow_mo=float(config["SlowMo"]),
        args=["--start-maximized"]
    )
    context = browser.new_context(
        base_url=common["Url"],
        no_viewport=True
    )
    context.set_default_navigation_timeout(float(config["DefaultNavigationTimeout"]))
    context.set_default_timeout(float(config["DefaultTimeout"]))

    page = context.new_page()
    page.goto(common["Url"])

    # Login once
    login_page = LoginPage(page)
    login_page.login_to_application(common["ValidUserName"], common["ValidPassword"])

    request.cls.page = page
    yield
    page.close()
    browser.close()
    playwright.stop()


# ======================
# Screenshot on Failure
# ======================

# We'll initialize this on first failure only
RUN_DIR = None

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    For failed tests only, save screenshot and error log under test_failures/run_<timestamp>/<test_name>/
    """
    global RUN_DIR
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call", "teardown") and report.failed:
        test_instance = item.instance
        if hasattr(test_instance, "page") and test_instance.page:
            page = test_instance.page

            # Create session folder on first failure only
            if RUN_DIR is None:
                now = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
                RUN_DIR = os.path.join("test_failures", now)
                os.makedirs(RUN_DIR, exist_ok=True)

            # Safe test name
            test_name = item.nodeid.replace("::", "_").replace("/", "_")
            test_folder = os.path.join(RUN_DIR, test_name)
            os.makedirs(test_folder, exist_ok=True)

            # Screenshot
            screenshot_path = os.path.join(test_folder, f"{test_name}.png")
            try:
                page.screenshot(path=screenshot_path, full_page=True, timeout=30000)
                print(f"[INFO] Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"[ERROR] Failed to capture screenshot: {e}")

            # Error log
            error_path = os.path.join(test_folder, f"{test_name}_error.txt")
            try:
                with open(error_path, "w", encoding="utf-8") as f:
                    f.write(report.longreprtext)
                print(f"[INFO] Error log saved: {error_path}")
            except Exception as e:
                print(f"[ERROR] Failed to save error log: {e}")




# ======================
# CLI Option for browser
# ======================

def pytest_addoption(parser):
    parser.addoption("--browser-name", action="store", default="chromium", help="Browser: chromium, firefox")
