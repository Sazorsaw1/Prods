import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        driver.implicitly_wait(0.5)

        dropdown_element = driver.find_element(By.NAME, "my-select")
        Select(dropdown_element).select_by_visible_text("One")

        text_box = driver.find_element(By.NAME, "my-text")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button")

        text_box.send_keys("Selenium")
        time.sleep(5)
        submit_button.click()

        message = driver.find_element(By.ID, "message")
        print(message.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
