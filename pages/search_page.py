from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage


class SearchPage(BasePage):
    # Локаторы для результатов поиска
    SEARCH_RESULTS_CONTAINER = (By.CSS_SELECTOR, ".search_results")  # Основной контейнер
    MOVIE_ITEMS = (By.CSS_SELECTOR, ".search_results .movie-item")  # Элементы фильмов
    MOVIE_TITLES = (By.CSS_SELECTOR, ".movie-item .title")  # Названия фильмов

    # Новые локаторы для блока "Скорее всего, вы ищете"
    MOST_LIKELY_RESULT = (By.CSS_SELECTOR, ".element.most_wanted")  # Блок "Скорее всего, вы ищете"
    MOST_LIKELY_TITLE = (By.CSS_SELECTOR, ".element.most_wanted .name a")  # Название фильма в основном результате
    SEARCH_RESULTS_LIST = (By.CSS_SELECTOR, ".search_results .element")  # Список всех результатов
    SEARCH_RESULT_TITLES = (By.CSS_SELECTOR, ".search_results .element .name a")  # Названия всех результатов

    # Локаторы для пустого поиска (обновлённые на основе HTML)
    RANDOM_MOVIE_BLOCK = (By.CSS_SELECTOR, ".randomMovie")  # Основной блок
    RANDOM_MOVIE_BUTTON = (By.CSS_SELECTOR, ".randomMovieButton .button")  # Конкретная кнопка
    NO_RESULTS_MESSAGE = (By.XPATH, "//*[contains(translate(text(), 'НИЧЕГО', 'ничего'), 'ничего не найдено')]")
    EMPTY_SEARCH_MESSAGE = (By.XPATH, "//*[contains(text(), 'Введите запрос') or contains(text(), 'заполните поле')]")

    # Локаторы для ошибок
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    # Новые методы для работы с блоком "Скорее всего, вы ищете"
    def is_most_likely_result_displayed(self, timeout=10):
        """Проверяет отображение блока 'Скорее всего, вы ищете'"""
        return self.is_element_visible(self.MOST_LIKELY_RESULT, timeout)

    def get_most_likely_title(self):
        """Возвращает название фильма в основном результате"""
        return self.find(self.MOST_LIKELY_TITLE).text

    # Обновленный метод для проверки наличия результатов
    def are_movies_found(self, timeout=5):
        """Проверяет, есть ли какие-либо результаты поиска (обновленная версия)"""
        try:
            return (self.is_most_likely_result_displayed(timeout) or
                    len(self.find_all(self.MOVIE_ITEMS, timeout)) > 0 or
                    len(self.find_all(self.SEARCH_RESULT_TITLES, timeout)) > 0)
        except:
            return False

    # Существующие методы остаются без изменений
    def wait_for_random_movie_block(self, timeout=10):
        """Новый метод: Явное ожидание появления блока случайного фильма"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.RANDOM_MOVIE_BLOCK)
            )
            return True
        except:
            return False

    def is_results_found(self, timeout=10):
        """Проверяет, отобразились ли результаты поиска"""
        try:
            return self.is_element_visible(self.SEARCH_RESULTS_CONTAINER, timeout)
        except:
            return False

    def is_movie_present(self, title, timeout=5):
        """Проверяет наличие конкретного фильма в результатах"""
        try:
            movies = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(self.MOVIE_TITLES)
            )
            return any(title.lower() in movie.text.lower() for movie in movies)
        except:
            return False

    def is_no_results_found(self, timeout=5):
        """Проверяет сообщение 'Ничего не найдено'"""
        try:
            return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout)
        except:
            return False

    def is_random_movie_suggested(self, timeout=10):
        """Проверяет отображение блока случайного фильма (обновлённый метод)"""
        try:
            return (self.is_element_visible(self.RANDOM_MOVIE_BLOCK, timeout) or
                    self.is_element_visible(self.RANDOM_MOVIE_BUTTON, timeout))
        except:
            return False

    def is_empty_search_message_displayed(self, timeout=5):
        """Проверяет сообщение о пустом запросе"""
        try:
            return self.is_element_visible(self.EMPTY_SEARCH_MESSAGE, timeout)
        except:
            return False

    def get_error_message(self, timeout=5):
        """Возвращает текст сообщения об ошибке"""
        try:
            return self.find(self.ERROR_MESSAGE, timeout).text
        except:
            return ""