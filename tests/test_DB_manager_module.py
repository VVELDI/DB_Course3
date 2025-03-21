import unittest
from unittest.mock import patch, Mock
from src.DB_manager_module import DBManager


class TestDBManager(unittest.TestCase):
    """
    Тесты для класса DBManager, который отвечает за управление данными в базе данных.
    """

    def setUp(self):
        """
        Инициализация объекта DBManager перед каждым тестом.
        """
        self.db_manager = DBManager()

    @patch('psycopg2.connect')
    def test_get_companies_and_vacancies_count(self, mock_connect):
        """
        Тестирование метода get_companies_and_vacancies_count.

        Мокируем подключение к базе данных и проверяем, что метод корректно возвращает
        список компаний и количество их вакансий.
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

        # Мокируем результат выполнения запроса
        mock_cursor.fetchall.return_value = [("Company A", 10), ("Company B", 5)]

        # Вызываем метод и проверяем результат
        result = self.db_manager.get_companies_and_vacancies_count()
        self.assertIn("Компании и количество вакансий", result)
        self.assertIn("Company A", result)
        self.assertIn("Company B", result)

    @patch('psycopg2.connect')
    def test_get_all_vacancies(self, mock_connect):
        """
        Тестирование метода get_all_vacancies.

        Мокируем подключение к базе данных и проверяем, что метод корректно возвращает
        список всех вакансий.
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

        # Мокируем результат выполнения запроса
        mock_cursor.fetchall.return_value = [
            ("Company A", "Python Developer", 125000, "http://example.com")
        ]

        # Вызываем метод и проверяем результат
        result = self.db_manager.get_all_vacancies()
        self.assertIn("Список всех вакансий", result)
        self.assertIn("Python Developer", result)

    @patch('psycopg2.connect')
    def test_get_avg_salary(self, mock_connect):
        """
        Тестирование метода get_avg_salary.

        Мокируем подключение к базе данных и проверяем, что метод корректно возвращает
        среднюю зарплату по вакансиям.
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

        # Мокируем результат выполнения запроса
        mock_cursor.fetchall.return_value = [(120000,)]

        # Вызываем метод и проверяем результат
        result = self.db_manager.get_avg_salary()
        self.assertIn("Средняя зарплата по вакансиям", result)
        self.assertIn("120000", result)

    @patch('psycopg2.connect')
    def test_get_vacancies_with_higher_salary(self, mock_connect):
        """
        Тестирование метода get_vacancies_with_higher_salary.

        Мокируем подключение к базе данных и проверяем, что метод корректно возвращает
        вакансии с зарплатой выше средней.
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

        # Мокируем результат выполнения запроса
        mock_cursor.fetchall.return_value = [
            ("1", "Python Developer", 100000, 150000, "Experience with Python", "http://example.com", "1")
        ]

        # Вызываем метод и проверяем результат
        result = self.db_manager.get_vacancies_with_higher_salary()
        self.assertIn("Вакансии с зарплатой выше среднего", result)
        self.assertIn("Python Developer", result)

    @patch('psycopg2.connect')
    def test_get_vacancies_with_keyword(self, mock_connect):
        """
        Тестирование метода get_vacancies_with_keyword.

        Мокируем подключение к базе данных и проверяем, что метод корректно возвращает
        вакансии по ключевому слову.
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

        # Мокируем результат выполнения запроса
        mock_cursor.fetchall.return_value = [
            ("1", "Python Developer", 100000, 150000, "Experience with Python", "http://example.com", "1")
        ]

        # Вызываем метод и проверяем результат
        result = self.db_manager.get_vacancies_with_keyword("Python")
        self.assertIn("Вакансии по ключевому слову", result)
        self.assertIn("Python Developer", result)