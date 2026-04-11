import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def _price_value(text):
    digits = re.sub(r"[^\d]", "", text)
    return int(digits or "0")


def _alert_text(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text


def _first_item_slug(driver, wait, timeout_seconds):
    checkbox = wait(driver, timeout_seconds).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid^="order-checkbox-"]')
        )
    )
    return checkbox.get_attribute("data-testid").replace("order-checkbox-", "")


def test_create_order_modal_opens_and_closes(
    driver, open_order_modal, wait, timeout_seconds
):
    modal = open_order_modal()
    assert modal.is_displayed()

    driver.find_element(By.ID, "cancelOrder").click()
    wait(driver, timeout_seconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="create-order-modal"]')
        )
    )


def test_submit_requires_table_selection(
    driver, open_order_modal, wait, timeout_seconds
):
    open_order_modal()
    driver.find_element(By.ID, "submitOrder").click()

    assert (
        _alert_text(driver, wait, timeout_seconds) == "Please select a table number."
    )


def test_submit_requires_menu_selection_after_table_pick(
    driver, open_order_modal, wait, timeout_seconds
):
    open_order_modal()
    Select(driver.find_element(By.ID, "tableNumber")).select_by_visible_text("Table 1")
    driver.find_element(By.ID, "submitOrder").click()

    assert (
        _alert_text(driver, wait, timeout_seconds)
        == "Please select at least one menu item."
    )


def test_selecting_item_and_increasing_quantity_updates_total(
    driver, open_order_modal, wait, timeout_seconds
):
    open_order_modal()

    slug = _first_item_slug(driver, wait, timeout_seconds)
    checkbox = driver.find_element(
        By.CSS_SELECTOR, f'[data-testid="order-checkbox-{slug}"]'
    )
    quantity = driver.find_element(
        By.CSS_SELECTOR, f'[data-testid="quantity-value-{slug}"]'
    )
    increase = driver.find_element(
        By.CSS_SELECTOR, f'[data-testid="increase-quantity-{slug}"]'
    )
    total = driver.find_element(By.ID, "totalPrice")

    assert total.text == "0"
    assert quantity.text == "1"

    checkbox.click()
    wait(driver, timeout_seconds).until(lambda browser: _price_value(total.text) > 0)
    selected_total = _price_value(total.text)

    increase.click()
    wait(driver, timeout_seconds).until(lambda browser: quantity.text == "2")
    wait(driver, timeout_seconds).until(
        lambda browser: _price_value(total.text) > selected_total
    )

    assert _price_value(total.text) > selected_total


def test_unchecking_item_resets_total_to_zero(
    driver, open_order_modal, wait, timeout_seconds
):
    open_order_modal()

    slug = _first_item_slug(driver, wait, timeout_seconds)
    checkbox = driver.find_element(
        By.CSS_SELECTOR, f'[data-testid="order-checkbox-{slug}"]'
    )
    total = driver.find_element(By.ID, "totalPrice")

    checkbox.click()
    wait(driver, timeout_seconds).until(lambda browser: _price_value(total.text) > 0)

    checkbox.click()
    wait(driver, timeout_seconds).until(lambda browser: total.text == "0")

    assert total.text == "0"
