import os

import pytest
from pytest_bdd import given, parsers, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

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


def pytest_html_report_title(report):
    report.title = "E-Restaurant Frontend Automation Report"


@given("the customer homepage is open")
def customer_homepage_is_open(driver):
    return driver


@then("the customer homepage shows the main actions")
def customer_homepage_shows_main_actions(driver, wait, timeout_seconds):
    assert driver.title == "E-Restaurant"

    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="menu-search-input"]')
        )
    )
    page_wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="menu-category-filter"]')
        )
    )

    assert driver.find_element(
        By.CSS_SELECTOR, '[data-testid="open-create-order-button"]'
    ).is_displayed()
    assert driver.find_element(
        By.CSS_SELECTOR, '[data-testid="open-check-order-button"]'
    ).is_displayed()
    assert len(
        driver.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')
    ) > 0


@when(parsers.parse('the user searches for "{search_term}"'))
def user_searches_for(driver, search_term):
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(search_term)


@then(parsers.parse('only menu cards matching "{search_term}" are shown'))
def only_matching_menu_cards_are_shown(driver, wait, timeout_seconds, search_term):
    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        lambda browser: len(
            browser.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')
        )
        > 0
        and all(
            search_term.lower() in card.get_attribute("data-menu-name").lower()
            for card in browser.find_elements(
                By.CSS_SELECTOR, '[data-testid^="menu-card-"]'
            )
        )
    )

    assert all(
        search_term.lower() in card.get_attribute("data-menu-name").lower()
        for card in driver.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')
    )


@then("the empty search state is shown")
def empty_search_state_is_shown(driver, wait, timeout_seconds):
    empty_state = wait(driver, timeout_seconds).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="menu-empty-state"]')
        )
    )
    assert "No menu items match your search." in empty_state.text


@when(parsers.parse('the user filters the menu by "{category_value}"'))
def user_filters_menu_by(driver, wait, timeout_seconds, category_value):
    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        lambda browser: browser.find_elements(
            By.CSS_SELECTOR, f'#categoryFilter option[value="{category_value}"]'
        )
    )
    Select(driver.find_element(By.ID, "categoryFilter")).select_by_value(category_value)


@then(parsers.parse('only "{category_value}" menu cards are shown'))
def only_category_menu_cards_are_shown(driver, wait, timeout_seconds, category_value):
    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        lambda browser: len(
            browser.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')
        )
        > 0
        and all(
            card.get_attribute("data-menu-category") == category_value
            for card in browser.find_elements(
                By.CSS_SELECTOR, '[data-testid^="menu-card-"]'
            )
        )
    )

    assert all(
        card.get_attribute("data-menu-category") == category_value
        for card in driver.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')
    )


@then("today's recommendation shows four menu cards")
def todays_recommendation_shows_four_menu_cards(driver, wait, timeout_seconds):
    page_wait = wait(driver, timeout_seconds)
    section = page_wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="todays-recommendation-container"]')
        )
    )
    page_wait.until(
        lambda browser: len(
            browser.find_elements(
                By.CSS_SELECTOR, '[data-testid^="todays-recommendation-card-"]'
            )
        )
        == 4
    )

    cards = driver.find_elements(
        By.CSS_SELECTOR, '[data-testid^="todays-recommendation-card-"]'
    )
    assert section.is_displayed()
    assert len(cards) == 4
    assert driver.find_element(
        By.XPATH, "//h2[normalize-space()=\"Today's Recommendation\"]"
    ).is_displayed()
    labels = driver.find_elements(
        By.XPATH,
        "//article[starts-with(@data-testid, 'todays-recommendation-card-')]//span[normalize-space()=\"Today's Recommendation\"]",
    )
    assert len(labels) == 4


@then("the people favorites section is visible")
def people_favorites_section_is_visible(driver, wait, timeout_seconds):
    section = wait(driver, timeout_seconds).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="peoples-favorites-container"]')
        )
    )
    assert section.is_displayed()
    assert driver.find_element(
        By.XPATH, "//h2[normalize-space()=\"People Favorites\"]"
    ).is_displayed()


@then("the chef's pick section is visible")
def chefs_pick_section_is_visible(driver, wait, timeout_seconds):
    section = wait(driver, timeout_seconds).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="chefs-pick-container"]')
        )
    )
    assert section.is_displayed()
    assert driver.find_element(
        By.XPATH, "//h2[normalize-space()=\"Chef's Pick\"]"
    ).is_displayed()


@when("the user opens the create order modal")
def user_opens_create_order_modal(open_order_modal):
    return open_order_modal()


@then("the create order modal is visible")
def create_order_modal_is_visible(driver):
    assert driver.find_element(
        By.CSS_SELECTOR, '[data-testid="create-order-modal"]'
    ).is_displayed()


@when("the user closes the create order modal")
def user_closes_create_order_modal(driver):
    driver.find_element(By.ID, "cancelOrder").click()


@then("the create order modal is closed")
def create_order_modal_is_closed(driver, wait, timeout_seconds):
    wait(driver, timeout_seconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="create-order-modal"]')
        )
    )


@when("the user submits the order without selecting a table")
def user_submits_order_without_selecting_table(driver):
    driver.find_element(By.ID, "submitOrder").click()


@then("an alert asks for a table number")
def alert_asks_for_table_number(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    assert alert.text == "Please select a table number."
    alert.accept()


@when("the user chooses Table 1")
def user_chooses_table_1(driver):
    Select(driver.find_element(By.ID, "tableNumber")).select_by_visible_text("Table 1")


@when("the user submits the order without selecting a menu item")
def user_submits_order_without_selecting_menu_item(driver):
    driver.find_element(By.ID, "submitOrder").click()


@then("an alert asks for at least one menu item")
def alert_asks_for_at_least_one_menu_item(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    assert alert.text == "Please select at least one menu item."
    alert.accept()


@when("the user selects the first available order item")
def user_selects_first_available_order_item(driver, wait, timeout_seconds):
    checkbox = wait(driver, timeout_seconds).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid^="order-checkbox-"]')
        )
    )
    checkbox.click()


@when("the user increases the first available order item quantity")
def user_increases_first_available_order_item_quantity(driver, wait, timeout_seconds):
    checkbox = wait(driver, timeout_seconds).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid^="order-checkbox-"]')
        )
    )
    slug = checkbox.get_attribute("data-testid").replace("order-checkbox-", "")
    driver.find_element(
        By.CSS_SELECTOR, f'[data-testid="increase-quantity-{slug}"]'
    ).click()


@then("the total price increases above zero")
def total_price_increases_above_zero(driver, wait, timeout_seconds):
    total = driver.find_element(By.ID, "totalPrice")
    wait(driver, timeout_seconds).until(
        lambda browser: int("".join(ch for ch in total.text if ch.isdigit()) or "0") > 0
    )
    assert int("".join(ch for ch in total.text if ch.isdigit()) or "0") > 0


@when("the user deselects the first available order item")
def user_deselects_first_available_order_item(driver, wait, timeout_seconds):
    checkbox = wait(driver, timeout_seconds).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid^="order-checkbox-"]')
        )
    )
    if not checkbox.is_selected():
        checkbox.click()
    checkbox.click()


@then("the total price returns to zero")
def total_price_returns_to_zero(driver, wait, timeout_seconds):
    total = driver.find_element(By.ID, "totalPrice")
    wait(driver, timeout_seconds).until(lambda browser: total.text == "0")
    assert total.text == "0"


@when("the user opens the check order modal")
def user_opens_check_order_modal(open_check_modal):
    return open_check_modal()


@then("the check order modal is visible")
def check_order_modal_is_visible(driver):
    assert driver.find_element(
        By.CSS_SELECTOR, '[data-testid="check-order-modal"]'
    ).is_displayed()


@when("the user closes the check order modal")
def user_closes_check_order_modal(driver):
    driver.find_element(By.ID, "cancelCheckOrder").click()


@then("the check order modal is closed")
def check_order_modal_is_closed(driver, wait, timeout_seconds):
    wait(driver, timeout_seconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="check-order-modal"]')
        )
    )


@when("the user checks an empty order ID")
def user_checks_an_empty_order_id(driver):
    driver.find_element(By.ID, "checkOrderBtn").click()


@then("an alert asks for an order ID")
def alert_asks_for_an_order_id(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    assert alert.text == "Please enter an Order ID"
    alert.accept()


@when(parsers.parse('the user enters "{order_id}" as the order ID'))
def user_enters_order_id(driver, order_id):
    order_input = driver.find_element(By.ID, "orderIdInput")
    order_input.clear()
    order_input.send_keys(order_id)


@when("the user checks the order status")
def user_checks_the_order_status(driver):
    driver.find_element(By.ID, "checkOrderBtn").click()


@then("an alert asks for the 6 digit order number")
def alert_asks_for_the_6_digit_order_number(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    assert alert.text == "Please enter the 6-digit number from your Order ID."
    alert.accept()
