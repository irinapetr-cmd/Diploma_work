from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import logging


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(type(self).__name__)

    def find(self, locator):
        """Поиск элемента с ожиданием его появления"""
        try:
            self.logger.info(f"Поиск элемента по локатору: {locator}")
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Элемент не найден: {locator}")
            self.take_screenshot("element_not_found")
            raise

    def find_all(self, locator):
        """Поиск всех элементов по локатору"""
        try:
            self.logger.info(f"Поиск всех элементов по локатору: {locator}")
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.warning(f"Элементы не найдены: {locator}")
            return []

    def click(self, locator):
        """Клик по элементу с ожиданием кликабельности"""
        try:
            self.logger.info(f"Клик по элементу: {locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            self.logger.error(f"Элемент не кликабелен: {locator}")
            self.take_screenshot("element_not_clickable")
            raise

    def type(self, locator, text):
        """Ввод текста в поле"""
        try:
            self.logger.info(f"Ввод текста '{text}' в элемент: {locator}")
            element = self.find(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Ошибка при вводе текста: {str(e)}")
            self.take_screenshot("text_input_error")
            raise

    def is_element_present(self, locator, timeout=5):
        """Проверка наличия элемента на странице"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator, timeout=5):
        """Проверка видимости элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, name):
        """Создание скриншота и прикрепление к Allure-отчету"""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=f"screenshot_{name}",
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Создан скриншот: {name}")

    def get_current_url(self):
        """Получение текущего URL"""
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание появления текста в URL"""
        try:
            self.wait.until(EC.url_contains(text))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator):
        """Прокрутка страницы к элементу"""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)