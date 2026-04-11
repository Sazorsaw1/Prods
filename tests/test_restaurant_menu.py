from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def _visible_menu_cards(driver):
    return driver.find_elements(By.CSS_SELECTOR, '[data-testid^="menu-card-"]')


def test_home_page_loads_with_primary_actions(driver, wait, timeout_seconds):
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
    assert len(_visible_menu_cards(driver)) > 0


def test_search_filters_to_matching_menu_cards(driver, wait, timeout_seconds):
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys("Avocado")

    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        lambda browser: len(_visible_menu_cards(browser)) > 0
        and all(
            "avocado" in card.get_attribute("data-menu-name").lower()
            for card in _visible_menu_cards(browser)
        )
    )

    assert all(
        "avocado" in card.get_attribute("data-menu-name").lower()
        for card in _visible_menu_cards(driver)
    )


def test_search_shows_empty_state_for_unknown_menu(driver, wait, timeout_seconds):
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys("RandomFood123")

    empty_state = wait(driver, timeout_seconds).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="menu-empty-state"]')
        )
    )

    assert "No menu items match your search." in empty_state.text


def test_category_filter_limits_results_to_selected_category(
    driver, wait, timeout_seconds
):
    filter_element = driver.find_element(By.ID, "categoryFilter")
    page_wait = wait(driver, timeout_seconds)
    page_wait.until(
        lambda browser: browser.find_elements(
            By.CSS_SELECTOR, '#categoryFilter option[value="dessert"]'
        )
    )

    Select(filter_element).select_by_value("dessert")

    page_wait.until(
        lambda browser: len(_visible_menu_cards(browser)) > 0
        and all(
            card.get_attribute("data-menu-category") == "dessert"
            for card in _visible_menu_cards(browser)
        )
    )

    assert all(
        card.get_attribute("data-menu-category") == "dessert"
        for card in _visible_menu_cards(driver)
    )
