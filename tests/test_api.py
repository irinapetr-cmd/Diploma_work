import pytest
import requests
from config.settings import API_URL, API_KEY
from config.test_data import SEARCH_QUERIES


class TestKinopoiskAPI:
    @pytest.mark.api
    def test_search_by_full_title(self):
        """Поиск по полному названию фильма"""
        params = {"query": SEARCH_QUERIES["full_title"]}
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{API_URL}v1.4/movie/search",
            params=params,
            headers=headers
        )

        assert response.status_code == 200
        assert SEARCH_QUERIES["full_title"].lower() in response.text.lower()

    @pytest.mark.api
    def test_search_by_partial_title(self):
        """Поиск по части названия фильма"""
        params = {"query": SEARCH_QUERIES["partial_title"]}
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{API_URL}v1.4/movie/search",
            params=params,
            headers=headers
        )

        assert response.status_code == 200
        assert len(response.json()["docs"]) > 0

    @pytest.mark.api
    def test_search_without_api_key(self):
        """Попытка поиска без API ключа"""
        params = {"query": SEARCH_QUERIES["full_title"]}
        headers = {"Content-Type": "application/json"}

        response = requests.get(
            f"{API_URL}v1.4/movie/search",
            params=params,
            headers=headers
        )

        response_data = response.json()
        assert response.status_code == 401
        assert "В запросе не указан токен!" in response_data["message"]

    @pytest.mark.api
    def test_search_with_invalid_year(self):
        """Поиск с несуществующим годом выпуска"""
        params = {"year": 9999}
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{API_URL}v1.4/movie",
            params=params,
            headers=headers
        )
        x=response.json()["message"][0]
        assert response.status_code == 400
        assert "диапазоне от 1874 до 2050" in x


    @pytest.mark.api
    def test_search_with_wrong_method(self):
        """Использование неправильного метода PUT вместо GET"""
        params = {"query": SEARCH_QUERIES["full_title"]}
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.put(
            f"{API_URL}v1.4/movie/search",
            params=params,
            headers=headers
        )

        assert response.status_code == 400