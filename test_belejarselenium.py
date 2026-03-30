from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pytest

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

# 1. Locate the dropdown element
dropdown_element = driver.find_element(By.NAME, "my-select")

# 2. Wrap it in a Select object
select = Select(dropdown_element)

# 3. Choose an option using one of three methods:
select.select_by_visible_text("One")


text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")

time.sleep(5)

submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

# driver.quit()

print(text)
