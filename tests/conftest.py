import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv(
    "RESTAURANT_BASE_URL",
    "https://restaurant-website-ten-bice.vercel.app/",
)
DEFAULT_TIMEOUT = int(os.getenv("RESTAURANT_UI_TIMEOUT", "15"))


def _headless_enabled():
    return os.getenv("SELENIUM_HEADLESS", "1").lower() not in {"0", "false", "no"}


def _build_chrome_options():
    options = webdriver.ChromeOptions()

    if _headless_enabled():
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=0")

    return options


@pytest.fixture(scope="function")
def wait():
    return WebDriverWait


@pytest.fixture(scope="function")
def timeout_seconds():
    return DEFAULT_TIMEOUT


@pytest.fixture(scope="function")
def driver():
    driver = None

    try:
        driver = webdriver.Chrome(options=_build_chrome_options())
        driver.implicitly_wait(0)
        driver.get(BASE_URL)

        page_wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        page_wait.until(
            lambda browser: browser.execute_script("return document.readyState")
            == "complete"
        )
        page_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="customer-home-page"]')
            )
        )
        page_wait.until(
            lambda browser: browser.find_elements(
                By.CSS_SELECTOR, '[data-testid^="menu-card-"]'
            )
            or browser.find_elements(
                By.CSS_SELECTOR, '[data-testid="menu-empty-state"]'
            )
        )

        yield driver
    finally:
        if driver is not None:
            driver.quit()


@pytest.fixture(scope="function")
def open_order_modal(driver, wait):
    def _open():
        driver.find_element(By.ID, "openModal").click()
        modal_wait = wait(driver, DEFAULT_TIMEOUT)
        modal_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="create-order-modal"]')
            )
        )
        modal_wait.until(
            lambda browser: browser.find_elements(
                By.CSS_SELECTOR, '[data-testid^="order-checkbox-"]'
            )
            or browser.find_elements(
                By.CSS_SELECTOR, '[data-testid="order-items-empty-state"]'
            )
        )
        return driver.find_element(
            By.CSS_SELECTOR, '[data-testid="create-order-modal"]'
        )

    return _open


@pytest.fixture(scope="function")
def open_check_modal(driver, wait):
    def _open():
        driver.find_element(By.ID, "openCheckModal").click()
        modal_wait = wait(driver, DEFAULT_TIMEOUT)
        modal_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="check-order-modal"]')
            )
        )
        return driver.find_element(
            By.CSS_SELECTOR, '[data-testid="check-order-modal"]'
        )

    return _open
