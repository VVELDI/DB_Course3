import unittest
from unittest.mock import patch, Mock
from src.api_module import FindVacancyFromHHApi, FindEmployerFromHHApi

class TestFindVacancyFromHHApi(unittest.TestCase):
    def setUp(self):
        self.api = FindVacancyFromHHApi()

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        # Мокируем ответ от API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Python Developer"},
                {"id": "2", "name": "Data Scientist"}
            ]
        }
        mock_get.return_value = mock_response

        # Вызываем метод и проверяем результат
        vacancies = self.api.get_vacancies("Python")
        self.assertEqual(len(vacancies), 40)
        self.assertEqual(vacancies[0]["name"], "Python Developer")
        self.assertEqual(vacancies[1]["name"], "Data Scientist")

    @patch('requests.get')
    def test_get_vacancies_by_employer_id(self, mock_get):
        # Мокируем ответ от API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Python Developer", "employer": {"id": "123"}},
                {"id": "2", "name": "Data Scientist", "employer": {"id": "123"}}
            ]
        }
        mock_get.return_value = mock_response

        # Вызываем метод и проверяем результат
        vacancies = self.api.get_vacancies_by_employer_id("123")
        self.assertEqual(len(vacancies), 20)
        self.assertEqual(vacancies[0]["name"], "Python Developer")
        self.assertEqual(vacancies[1]["name"], "Data Scientist")

class TestFindEmployerFromHHApi(unittest.TestCase):
    def setUp(self):
        self.api = FindEmployerFromHHApi()

    @patch('requests.get')
    def test_get_employer_info(self, mock_get):
        # Мокируем ответ от API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Company A"},
                {"id": "2", "name": "Company B"}
            ]
        }
        mock_get.return_value = mock_response

        # Вызываем метод и проверяем результат
        employers = self.api.get_employer_info(2, "Company")
        self.assertEqual(len(employers), 40)
        self.assertEqual(employers[0]["name"], "Company A")
        self.assertEqual(employers[1]["name"], "Company B")
