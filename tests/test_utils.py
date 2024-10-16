import unittest
from unittest.mock import patch, MagicMock
import requests
from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch('src.api.requests.get')
    def test_get_vacancies_success(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            'items': [
                {'name': 'Python Developer', 'url': 'https://example.com/vacancy/1'},
                {'name': 'Backend Developer', 'url': 'https://example.com/vacancy/2'}
            ]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        # Act
        result = api.get_vacancies('Python разработчик')

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Python Developer')
        self.assertEqual(result[1]['name'], 'Backend Developer')

    @patch('src.api.requests.get')
    def test_get_vacancies_empty(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            'items': []
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        # Act
        result = api.get_vacancies('Non-existent job')

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch('src.api.requests.get')
    def test_get_vacancies_api_error(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        # Act & Assert
        with self.assertRaises(requests.exceptions.HTTPError):
            api.get_vacancies('Python разработчик')


if __name__ == '__main__':
    unittest.main()
