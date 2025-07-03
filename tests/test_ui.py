import pytest
import allure
from pages.main_page import MainPage
from pages.search_page import SearchPage
from config.settings import BASE_URL
from config.test_data import TEST_USER, SEARCH_QUERIES


@pytest.mark.ui
@allure.feature("UI Тесты Кинопоиска")
class TestKinopoiskUI:
    @allure.story("Поиск")
    @allure.title("Поиск фильма по полному названию: {SEARCH_QUERIES['full_title']}")
    def test_search_by_full_title(self, browser):
        with allure.step("Инициализация страниц"):
            main_page = MainPage(browser)
            search_page = SearchPage(browser)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step(f"Выполнить поиск фильма: {SEARCH_QUERIES['full_title']}"):
            main_page.search_for(SEARCH_QUERIES["full_title"])

        with allure.step("Проверить результаты поиска"):
            assert search_page.is_results_found(), "Результаты поиска не найдены"

    @allure.story("Поиск")
    @allure.title("Поиск фильма по части названия: {SEARCH_QUERIES['partial_title']}")
    def test_search_by_partial_title(self, browser):
        with allure.step("Инициализация страниц"):
            main_page = MainPage(browser)
            search_page = SearchPage(browser)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step(f"Выполнить поиск по части названия: {SEARCH_QUERIES['partial_title']}"):
            main_page.search_for(SEARCH_QUERIES["partial_title"])

        with allure.step("Проверить результаты поиска"):
            # Проверяем, что появился блок "Скорее всего, вы ищете"
            assert search_page.is_most_likely_result_displayed(), "Блок с наиболее вероятным результатом не отображается"

            # Проверяем, что в этом блоке есть искомый фильм
            most_likely_title = search_page.get_most_likely_title()
            assert SEARCH_QUERIES["partial_title"].lower() in most_likely_title.lower(), (
                f"Ожидалось найти '{SEARCH_QUERIES['partial_title']}' в '{most_likely_title}'"
            )

            # Прикрепляем скриншот для отчета
            allure.attach(
                browser.get_screenshot_as_png(),
                name="partial_search_result",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.story("Поиск")
    @allure.title("Поиск несуществующего фильма")
    def test_search_nonexistent_movie(self, browser):
        with allure.step("Инициализация страниц"):
            main_page = MainPage(browser)
            search_page = SearchPage(browser)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск несуществующего фильма"):
            main_page.search_for("НесуществующийФильм123")

        with allure.step("Проверить сообщение об отсутствии результатов"):
            assert search_page.is_no_results_found(), "Не отображается сообщение 'Ничего не найдено'"
            allure.attach(
                browser.get_screenshot_as_png(),
                name="no_results_message",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.story("Валидация")
    @allure.title("Поиск с пустым запросом")
    def test_empty_search(self, browser):
        with allure.step("Инициализация страниц"):
            main_page = MainPage(browser)
            search_page = SearchPage(browser)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск с пустым запросом"):
            main_page.search_for("")

        with allure.step("Ожидать появления блока случайного фильма"):
            assert search_page.wait_for_random_movie_block(), (
                    "Блок случайного фильма не появился в течение 10 секунд. " +
                    f"Текущий URL: {browser.current_url}"
            )

        with allure.step("Проверить элементы блока"):
            assert search_page.is_element_visible(search_page.RANDOM_MOVIE_BUTTON), \
                "Не найдена кнопка в блоке случайного фильма"

        with allure.step("Диагностика"):
            allure.attach(
                browser.get_screenshot_as_png(),
                name="empty_search_result",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                browser.page_source,
                name="page_source",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("Валидация")
    @allure.title("Поиск с специальными символами")
    def test_search_with_special_chars(self, browser):
        with allure.step("Инициализация страниц"):
            main_page = MainPage(browser)
            search_page = SearchPage(browser)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск с спецсимволами @@@###"):
            main_page.search_for("@@@###")

        with allure.step("Проверить сообщение 'Ничего не найдено'"):
            # Явное ожидание сообщения
            assert search_page.is_no_results_found(timeout=10), \
                "Не отображается сообщение 'Ничего не найдено'"

            # Дополнительная проверка текста сообщения
            no_results_text = search_page.find(search_page.NO_RESULTS_MESSAGE).text
            assert "ничего не найдено" in no_results_text.lower(), \
                f"Текст сообщения не соответствует ожидаемому: '{no_results_text}'"

        with allure.step("Проверить отсутствие результатов"):
            assert not search_page.are_movies_found(), \
                "Найдены неожиданные результаты при поиске спецсимволов"

        with allure.step("Диагностическая информация"):
            # Прикрепляем скриншот и HTML для отладки
            allure.attach(
                browser.get_screenshot_as_png(),
                name="special_chars_search_result",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                browser.page_source,
                name="page_source",
                attachment_type=allure.attachment_type.TEXT
            )