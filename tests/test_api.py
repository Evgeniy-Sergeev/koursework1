import unittest
from unittest.mock import patch, Mock
import requests
from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    @patch('src.api.requests.get')
    def test_get_vacancies_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            'items': [
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
        }
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies('Python Developer')
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]['name'], 'Python Developer')
        self.assertEqual(vacancies[1]['name'], 'Junior Python Developer')

    @patch('src.api.requests.get')
    def test_get_vacancies_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        with self.assertRaises(requests.exceptions.HTTPError):
            hh_api.get_vacancies('Python Developer')


if __name__ == '__main__':
    unittest.main()
