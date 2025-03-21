import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.files_module import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver(unittest.TestCase):
    """
    Тесты для класса JSONSaver, который отвечает за сохранение и управление вакансиями в JSON-файле.
    """

    def setUp(self):
        """
        Инициализация объекта JSONSaver и тестовой вакансии перед каждым тестом.
        """
        self.saver = JSONSaver()
        # Создаем объект Vacancy с правильными аргументами
        self.vacancy = Vacancy(
            vacancy_name="Python Developer",
            vacancy_url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            requirement="Experience with Python",
            vacancy_id="123456789",  # Должно быть 9 символов
            employer_id="1",
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_to_json_file(self, mock_json_dump, mock_file_open):
        """
        Тестирование метода save_to_json_file.

        Мокируем запись в файл и проверяем, что данные вакансий корректно сохраняются в JSON-файл.
        """
        # Мокируем список вакансий
        vac_obj_list = [self.vacancy]

        # Вызываем метод и проверяем, что файл открывается и данные записываются
        self.saver.save_to_json_file(vac_obj_list)
        mock_file_open.assert_called_once_with(self.saver.path, mode="w")
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": "987654321", "name": "Java Developer"}]))
    @patch("json.dump")
    def test_add_vacancy(self, mock_json_dump, mock_file_open):
        """
        Тестирование метода add_vacancy.

        Мокируем чтение и запись в файл и проверяем, что вакансия корректно добавляется в JSON-файл.
        """
        # Вызываем метод и проверяем, что вакансия добавляется
        result = self.saver.add_vacancy(self.vacancy)
        mock_file_open.assert_called_with(self.saver.path, mode="r+")
        mock_json_dump.assert_called_once()
        self.assertEqual(result, None)  # Вакансия успешно добавлена

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": "123456789", "name": "Python Developer"}]))
    @patch("json.dump")
    def test_add_vacancy_already_exists(self, mock_json_dump, mock_file_open):
        """
        Тестирование метода add_vacancy, когда вакансия уже существует.

        Мокируем чтение и запись в файл и проверяем, что вакансия не добавляется, если она уже есть в файле.
        """
        # Вызываем метод и проверяем, что вакансия не добавляется, если уже существует
        result = self.saver.add_vacancy(self.vacancy)
        mock_file_open.assert_called_with(self.saver.path, mode="r+")
        mock_json_dump.assert_not_called()
        self.assertEqual(result, "Vacancy already in data")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": "123456789", "name": "Python Developer"}]))
    @patch("json.dump")
    def test_delete_vacancy(self, mock_json_dump, mock_file_open):
        """
        Тестирование метода delete_vacancy.

        Мокируем чтение и запись в файл и проверяем, что вакансия корректно удаляется из JSON-файла.
        """
        # Вызываем метод и проверяем, что вакансия удаляется
        result = self.saver.delete_vacancy(self.vacancy)
        mock_file_open.assert_called_with(self.saver.path, mode="r+")
        mock_json_dump.assert_called_once()
        self.assertEqual(result, "Vacancy deleted successfully")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": "987654321", "name": "Java Developer"}]))
    @patch("json.dump")
    def test_delete_vacancy_not_found(self, mock_json_dump, mock_file_open):
        """
        Тестирование метода delete_vacancy, когда вакансия не найдена.

        Мокируем чтение и запись в файл и проверяем, что вакансия не удаляется, если её нет в файле.
        """
        # Вызываем метод и проверяем, что вакансия не удаляется, если её нет в файле
        result = self.saver.delete_vacancy(self.vacancy)
        mock_file_open.assert_called_with(self.saver.path, mode="r+")
        mock_json_dump.assert_not_called()
        self.assertEqual(result, "Vacancy is not in data")