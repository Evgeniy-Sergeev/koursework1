import unittest
from unittest.mock import patch


class TestUserInteraction(unittest.TestCase):
    @patch('builtins.input',
           side_effect=['Python разработчик', '3', 'удаленная работа', '100000-150000', 'ключевое слово'])
    @patch('builtins.print')
    @patch('src.storage.JSONSaver.get_vacancies')
    @patch('src.storage.JSONSaver.add_vacancy')
    @patch('src.api.HeadHunterAPI.get_vacancies')
    def test_user_interaction(self, mock_get_vacancies_from_api, mock_add_vacancy, mock_get_vacancies, mock_print,
                              mock_input):
        mock_get_vacancies_from_api.return_value = [
            {
                'name': 'Python Developer',
                'alternate_url': 'http://example.com/1',
                'salary': {
                    'from': 120000,
                    'to': 150000
                },
                'snippet': {
                    'responsibility': 'Development of Python applications.'
                }
            },
            {
                'name': 'Junior Python Developer',
                'alternate_url': 'http://example.com/2',
                'salary': {
                    'from': 90000,
                    'to': 110000
                },
                'snippet': {
                    'responsibility': 'Assisting in Python development.'
                }
            }
        ]

        mock_get_vacancies.return_value = [
            {
                'title': 'Python Developer',
                'url': 'http://example.com/1',
                'salary': {
                    'from': 120000,
                    'to': 150000
                },
                'description': 'Development of Python applications.'
            },
            {
                'title': 'Junior Python Developer',
                'url': 'http://example.com/2',
                'salary': {
                    'from': 90000,
                    'to': 110000
                },
                'description': 'Assisting in Python development.'
            }
        ]


if __name__ == '__main__':
    unittest.main()
