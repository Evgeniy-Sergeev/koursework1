import json
from abc import abstractmethod


class VacancyStorage:
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class JSONSaver(VacancyStorage):
    def __init__(self, file_path: str = 'vacancies.json'):
        self.__file_path = file_path

    def add_vacancy(self, vacancy):
        vacancies = self.get_vacancies()
        if vacancy.url not in [v['url'] for v in vacancies]:
            vacancies.append({
                'title': vacancy.title,
                'url': vacancy.url,
                'salary': vacancy.salary,
                'description': vacancy.description
            })
        self._save_to_file(vacancies)

    def get_vacancies(self):
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self, vacancies):
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
