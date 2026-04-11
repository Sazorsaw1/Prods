from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def _alert_text(driver, wait, timeout_seconds):
    alert = wait(driver, timeout_seconds).until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text


def test_check_order_modal_opens_and_closes(
    driver, open_check_modal, wait, timeout_seconds
):
    modal = open_check_modal()
    assert modal.is_displayed()

    driver.find_element(By.ID, "cancelCheckOrder").click()
    wait(driver, timeout_seconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="check-order-modal"]')
        )
    )


def test_check_order_requires_input(driver, open_check_modal, wait, timeout_seconds):
    open_check_modal()
    driver.find_element(By.ID, "checkOrderBtn").click()

    assert _alert_text(driver, wait, timeout_seconds) == "Please enter an Order ID"


def test_check_order_rejects_non_six_digit_input(
    driver, open_check_modal, wait, timeout_seconds
):
    open_check_modal()
    driver.find_element(By.ID, "orderIdInput").send_keys("123")
    driver.find_element(By.ID, "checkOrderBtn").click()

    assert (
        _alert_text(driver, wait, timeout_seconds)
        == "Please enter the 6-digit number from your Order ID."
    )
