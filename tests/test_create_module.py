import unittest
from unittest.mock import patch, Mock
from src.DB_Create_module import DBConnection


class TestDBConnection(unittest.TestCase):
    """
    Тесты для класса DBConnection, который отвечает за взаимодействие с базой данных.
    """

    def setUp(self):
        """
        Инициализация объекта DBConnection перед каждым тестом.
        """
        self.db = DBConnection()

    @patch('psycopg2.connect')
    def test_connect_to_db(self, mock_connect):
        """
        Тестирование метода connect_to_db.

        Мокируем подключение к базе данных и проверяем, что метод корректно подключается к БД.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = Mock()

        # Вызываем метод и проверяем, что подключение произошло
        self.db.connect_to_db("SELECT 1;")
        mock_connect.assert_called_once()

    @patch('psycopg2.connect')
    def test_create_db(self, mock_connect):
        """
        Тестирование метода create_db.

        Мокируем подключение к базе данных и проверяем, что запросы на создание БД выполнены.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = Mock()

        # Вызываем метод и проверяем, что запросы на создание базы данных выполнены
        self.db.create_db()
        self.assertEqual(mock_conn.cursor().execute.call_count, 2)

    @patch('psycopg2.connect')
    def test_db_creating_employers(self, mock_connect):
        """
        Тестирование метода db_creating_employers.

        Мокируем подключение к базе данных и проверяем, что запрос на создание таблицы работодателей выполнен.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = Mock()

        # Вызываем метод и проверяем, что запрос на создание таблицы выполнен
        self.db.db_creating_employers()
        mock_conn.cursor().execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_db_filling_columns_for_emps(self, mock_connect):
        """
        Тестирование метода db_filling_columns_for_emps.

        Мокируем подключение к базе данных и проверяем, что данные о работодателях корректно вставляются в таблицу.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = Mock()

        # Тестовые данные
        employers_id_list = ["1", "2"]
        employers_list = [
            {"id": "1", "name": "Company A", "open_vacancies": 10},
            {"id": "2", "name": "Company B", "open_vacancies": 5},
        ]

        # Вызываем метод и проверяем, что запрос на вставку выполнен
        self.db.db_filling_columns_for_emps(employers_id_list, employers_list)
        self.assertEqual(mock_conn.cursor().execute.call_count, 2)

    @patch('psycopg2.connect')
    def test_db_creating_vacancies(self, mock_connect):
        """
        Тестирование метода db_creating_vacancies.

        Мокируем подключение к базе данных и проверяем, что запрос на создание таблицы вакансий выполнен.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = Mock()

        # Вызываем метод и проверяем, что запрос на создание таблицы выполнен
        self.db.db_creating_vacancies()
        mock_conn.cursor().execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_db_filling_vacancies(self, mock_connect):
        """
        Тестирование метода db_filling_vacancies.

        Мокируем подключение к базе данных и проверяем, что данные о вакансиях корректно вставляются в таблицу.
        """
        # Мокируем подключение к базе данных
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Добавляем поддержку контекстного менеджера
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=None)

        # Тестовые данные
        vacancies_list = [
            {
                "id": "1",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "Experience with Python"},
                "url": "http://example.com",
                "employer": {"id": "1"},
            }
        ]

        # Вызываем метод и проверяем, что запрос на вставку выполнен
        self.db.db_filling_vacancies(vacancies_list)
        mock_cursor.execute.assert_called_once()