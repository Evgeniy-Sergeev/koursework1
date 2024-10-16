import unittest
import os
import json
from src.storage import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        self.test_file_path = 'test_vacancies.json'
        self.storage = JSONSaver(file_path=self.test_file_path)
        self.vacancy1 = Vacancy('Python Developer', 'http://example.com/1', '120000-150000',
                                'Development of Python applications.')
        self.vacancy2 = Vacancy('Junior Developer', 'http://example.com/2', '90000-110000',
                                'Assisting in Python development.')

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_add_vacancy(self):
        self.storage.add_vacancy(self.vacancy1)
        vacancies = self.storage.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['title'], 'Python Developer')
        self.assertEqual(vacancies[0]['url'], 'http://example.com/1')
        self.assertEqual(vacancies[0]['salary'], '120000-150000')
        self.assertEqual(vacancies[0]['description'], 'Development of Python applications.')

    def test_add_duplicate_vacancy(self):
        self.storage.add_vacancy(self.vacancy1)
        self.storage.add_vacancy(self.vacancy1)
        vacancies = self.storage.get_vacancies()
        self.assertEqual(len(vacancies), 1)

    def test_get_vacancies_empty(self):
        vacancies = self.storage.get_vacancies()
        self.assertEqual(vacancies, [])

    def test_get_vacancies(self):
        self.storage.add_vacancy(self.vacancy1)
        self.storage.add_vacancy(self.vacancy2)
        vacancies = self.storage.get_vacancies()
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]['title'], 'Python Developer')
        self.assertEqual(vacancies[1]['title'], 'Junior Developer')

    def test_save_to_file(self):
        self.storage.add_vacancy(self.vacancy1)
        with open(self.test_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['title'], 'Python Developer')


if __name__ == '__main__':
    unittest.main()
