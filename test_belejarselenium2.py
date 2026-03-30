import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

@pytest.fixture(scope="session")
def driver():
    """Fixture to initialize and close the browser."""
    options = webdriver.ChromeOptions()
    # Note: 'detach' is usually False in automated testing to keep the environment clean
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")  
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def fresh_driver():
    """Opens a brand new browser for every test that uses it."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_web_form_opening(driver):
    # 1. Navigate
    assert "Web form" in driver.title

def test_dropdown_interaction(driver):  
    # 2. Interact with Dropdown
    dropdown_element = driver.find_element(By.NAME, "my-select")
    select = Select(dropdown_element)
    select.select_by_visible_text("One")
    assert select.first_selected_option.text == "One"


def test_input_text(driver):  
    # 3. Input Text
    text_box = driver.find_element(By.NAME, "my-text")
    text_box.send_keys("Selenium")
    
    # 4. Your requested pause
    # time.sleep(2)
    assert text_box.get_attribute("value") == "Selenium"

def test_input_password(driver):  
    # 3. Input Text
    password_box = driver.find_element(By.NAME, "my-password")
    password_box.send_keys("Kitaro")
    
    # 4. Your requested pause
    # time.sleep(2)
    assert password_box.get_attribute("value") == "Kitaro"

def test_readonly_inputs(driver):

    # 5. Target the Readonly input
    readonly_box = driver.find_element(By.NAME, "my-readonly")
    
    # Verify it is actually readonly
    assert readonly_box.get_attribute("readonly") == "true"

def test_disabled_inputs(driver):
    # 6. Target the Disabled input
    disabled_box = driver.find_element(By.NAME, "my-disabled")
    
    # Verify it is disabled
    assert not disabled_box.is_enabled()

def test_submit_button(driver):
    # 7. Submit
    submit_button = driver.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()



def test_web_form_submission(fresh_driver):
    # 1. Navigate
    fresh_driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    
# Interaction
    Select(fresh_driver.find_element(By.NAME, "my-select")).select_by_visible_text("One")
    text_box= fresh_driver.find_element(By.NAME, "my-text")
    password_box= fresh_driver.find_element(By.NAME, "my-password")
    readonly_box = fresh_driver.find_element(By.NAME, "my-readonly")
    disabled_box = fresh_driver.find_element(By.NAME, "my-disabled")
    
    assert readonly_box.get_attribute("readonly") == "true", "Readonly box should be locked!"
    assert not disabled_box.is_enabled(), "Disabled box should not be interactable!"
    text_box.send_keys("Selenium")
    password_box.send_keys("Kitaro")

   
    time.sleep(3)
    fresh_driver.find_element(By.CSS_SELECTOR, "button").click()

    # Verification
    message = fresh_driver.find_element(By.ID, "message")
    assert message.text == "Received!"