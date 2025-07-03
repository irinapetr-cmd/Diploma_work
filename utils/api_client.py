# utils/api_client.py
import requests
from config.settings import API_URL, API_KEY


class KinopoiskAPIClient:
    def __init__(self):
        self.base_url = API_URL
        self.headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

    def search_movies(self, query):
        """Поиск фильмов по названию"""
        params = {"query": query}
        response = requests.get(
            f"{self.base_url}v1.4/movie/search",
            params=params,
            headers=self.headers
        )
        return response

    def get_movie_by_id(self, movie_id):
        """Получение фильма по ID"""
        response = requests.get(
            f"{self.base_url}v1.4/movie/{movie_id}",
            headers=self.headers
        )
        return response

    def get_movies_by_year(self, year):
        """Фильтрация по году выпуска"""
        params = {"year": year}
        response = requests.get(
            f"{self.base_url}v1.4/movie",
            params=params,
            headers=self.headers
        )
        return response