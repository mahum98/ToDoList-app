# selenium_tests.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_dummy_ui():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")  # Make sure app is running locally for this to work
    time.sleep(2)
    assert "ToDo" in driver.title  # Adjust based on your app title
    driver.quit()

if __name__ == "__main__":
    test_dummy_ui()
