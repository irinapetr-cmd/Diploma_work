import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def browser():
    # Настройка Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()