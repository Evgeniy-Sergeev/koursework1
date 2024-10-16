import requests
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_text: str, area: int = 1, per_page: int = 10) -> list:
        pass


class HeadHunterAPI(VacancyAPI):
    __BASE_URL = 'https://api.hh.ru/vacancies'

    def __connect(self):
        return self.__BASE_URL

    def get_vacancies(self, search_text: str, area: int = 1, per_page: int = 10) -> list:
        url = self.__connect()
        params = {'text': search_text, 'area': area, 'per_page': per_page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
