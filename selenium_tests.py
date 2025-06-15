
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def test_page_title():
    driver = setup_driver()
    driver.get("http://localhost:5000")
    assert "ToDo" in driver.title or driver.title != "", "Title is missing"
    print("✅ Page title test passed")
    driver.quit()

def test_add_task():
    driver = setup_driver()
    driver.get("http://localhost:5000")
    task_input = driver.find_element(By.NAME, "task")  # Adjust name attr if needed
    task_input.send_keys("Test Task")
    task_input.send_keys(Keys.RETURN)
    time.sleep(1)
    tasks = driver.find_elements(By.CLASS_NAME, "task")  # Adjust class if needed
    assert any("Test Task" in t.text for t in tasks), "Task not added"
    print("✅ Add task test passed")
    driver.quit()

if __name__ == "__main__":
    test_page_title()
    test_add_task()
