import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def test_vacancy_creation(self):
        vacancy = Vacancy('Python Developer', 'http://example.com', '120000-150000',
                          'Development of Python applications.')
        self.assertEqual(vacancy.title, 'Python Developer')
        self.assertEqual(vacancy.url, 'http://example.com')
        self.assertEqual(vacancy.salary, '120000-150000')
        self.assertEqual(vacancy.description, 'Development of Python applications.')

    def test_vacancy_title_validation(self):
        with self.assertRaises(ValueError):
            Vacancy('', 'http://example.com', '120000-150000', 'Description')

    def test_vacancy_salary_validation(self):
        vacancy = Vacancy('Python Developer', 'http://example.com', 'Зарплата не указана', 'Description')
        self.assertEqual(vacancy.salary, '0')

    def test_vacancy_repr(self):
        vacancy = Vacancy('Python Developer', 'http://example.com', '120000-150000', 'Description')
        self.assertEqual(repr(vacancy), 'Python Developer (120000-150000) - http://example.com')

    def test_vacancy_comparison(self):
        vacancy1 = Vacancy('Python Developer', 'http://example.com/1', '120000-150000', 'Description')
        vacancy2 = Vacancy('Junior Developer', 'http://example.com/2', '90000-110000', 'Description')
        vacancy3 = Vacancy('Senior Developer', 'http://example.com/3', 'Зарплата не указана', 'Description')

        self.assertTrue(vacancy2 < vacancy1)
        self.assertTrue(vacancy3 < vacancy1)
        self.assertTrue(vacancy3 < vacancy2)

    def test_vacancy_equality(self):
        vacancy1 = Vacancy('Python Developer', 'http://example.com/1', '120000-150000', 'Description')
        vacancy2 = Vacancy('Another Developer', 'http://example.com/2', '120000-150000', 'Another Description')
        self.assertEqual(vacancy1, vacancy2)


if __name__ == '__main__':
    unittest.main()
