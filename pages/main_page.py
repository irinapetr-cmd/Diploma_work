# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class MainPage(BasePage):
    # Ваши актуальные локаторы
    LOGIN_BUTTON = (By.CLASS_NAME, "styles_loginButton__LWZQp")  # Кнопка "Войти"
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='text']")  # Поле поиска
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[aria-label='Найти']")  # Кнопка поиска

    # Дополнительные локаторы (нужно уточнить на сайте)
    USER_PROFILE = (By.CSS_SELECTOR, ".header__user-name")  # Профиль пользователя
    SUBSCRIPTION_LINK = (By.LINK_TEXT, "Подписки")  # Ссылка на подписки
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".logout-button")  # Кнопка выхода

    def open(self):
        """Открытие главной страницы"""
        self.driver.get("https://www.kinopoisk.ru/")
        return self

    def click_login(self):
        """Клик по кнопке 'Войти' с ожиданием"""
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        return self

    def search_for(self, query):
        """Выполнение поиска"""
        self.type(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return self

    def is_user_logged_in(self):
        """Проверка авторизации"""
        try:
            return self.find(self.USER_PROFILE).is_displayed()
        except:
            return False

    def open_subscription_page(self):
        """Открытие страницы подписок"""
        self.click(self.SUBSCRIPTION_LINK)
        return self

    def logout(self):
        """Выход из системы"""
        self.click(self.USER_PROFILE)
        self.click(self.LOGOUT_BUTTON)
        return self