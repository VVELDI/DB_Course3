import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    """
    Тесты для класса Vacancy.
    Проверяет инициализацию объекта, преобразование JSON-данных и получение информации о вакансии.
    """

    def setUp(self):
        """
        Инициализация тестовых данных.
        Создает пример JSON-вакансии для использования в тестах.
        """
        # Пример JSON-вакансии
        self.json_vacancy = {
            "name": "Python Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Experience with Python"},
            "id": "123456789",
            "employer": {"id": "1"},
        }

    def test_vacancy_initialization(self):
        """
        Тест инициализации объекта Vacancy.

        Проверяет, что атрибуты объекта Vacancy устанавливаются правильно.
        """
        vacancy = Vacancy(
            vacancy_name="Python Developer",
            vacancy_url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            requirement="Experience with Python",
            vacancy_id="123456789",
            employer_id="1",
        )

        # Проверяем, что атрибуты объекта установлены правильно
        self.assertEqual(vacancy._Vacancy__vacancy_name, "Python Developer")
        self.assertEqual(vacancy._Vacancy__vacancy_url, "http://example.com")
        self.assertEqual(vacancy._Vacancy__salary_from, 100000)
        self.assertEqual(vacancy._Vacancy__salary_to, 150000)
        self.assertEqual(vacancy._Vacancy__requirement, "Experience with Python")
        self.assertEqual(vacancy._Vacancy__id, "123456789")
        self.assertEqual(vacancy._Vacancy__employer_id, "1")

    def test_vacancy_initialization_with_missing_data(self):
        """
        Тест инициализации объекта Vacancy с отсутствующими данными.

        Проверяет, что значения по умолчанию устанавливаются правильно.
        """
        vacancy = Vacancy(
            vacancy_name="Python Developer",
            vacancy_url=None,
            salary_from=None,
            salary_to=None,
            requirement=None,
            vacancy_id="123",
            employer_id="1",
        )

        # Проверяем, что значения по умолчанию установлены правильно
        self.assertEqual(vacancy._Vacancy__vacancy_url, "Ссылка не указана")
        self.assertEqual(vacancy._Vacancy__salary_from, 0)
        self.assertEqual(vacancy._Vacancy__salary_to, 0)
        self.assertEqual(vacancy._Vacancy__requirement, "Требования не указаны")
        self.assertEqual(vacancy._Vacancy__id, "Unknown")

    def test_cast_to_object_list(self):
        """
        Тест преобразования JSON-вакансий в список объектов Vacancy.

        Проверяет, что метод корректно преобразует JSON-данные в список объектов Vacancy.
        """
        json_vacancies = [self.json_vacancy]
        vacancies_list = Vacancy.cast_to_object_list(json_vacancies)

        # Проверяем, что список содержит один объект Vacancy
        self.assertEqual(len(vacancies_list), 1)
        self.assertIsInstance(vacancies_list[0], Vacancy)

        # Проверяем, что данные объекта Vacancy соответствуют JSON-вакансии
        self.assertEqual(vacancies_list[0]._Vacancy__vacancy_name, "Python Developer")
        self.assertEqual(vacancies_list[0]._Vacancy__vacancy_url, "http://example.com")
        self.assertEqual(vacancies_list[0]._Vacancy__salary_from, 100000)
        self.assertEqual(vacancies_list[0]._Vacancy__salary_to, 150000)
        self.assertEqual(vacancies_list[0]._Vacancy__requirement, "Experience with Python")
        self.assertEqual(vacancies_list[0]._Vacancy__id, "123456789")
        self.assertEqual(vacancies_list[0]._Vacancy__employer_id, "1")

    def test_get_vacancy_info(self):
        """
        Тест свойства get_vacancy_info.

        Проверяет, что свойство возвращает информацию о вакансии в виде словаря.
        """
        vacancy = Vacancy(
            vacancy_name="Python Developer",
            vacancy_url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            requirement="Experience with Python",
            vacancy_id="123456789",
            employer_id="1",
        )

        # Получаем информацию о вакансии в виде словаря
        vacancy_info = vacancy.get_vacancy_info

        # Проверяем, что словарь содержит правильные данные
        self.assertEqual(vacancy_info["name"], "Python Developer")
        self.assertEqual(vacancy_info["url"], "http://example.com")
        self.assertEqual(vacancy_info["salary_from"], 100000)
        self.assertEqual(vacancy_info["salary_to"], 150000)
        self.assertEqual(vacancy_info["requirement"], "Experience with Python")
        self.assertEqual(vacancy_info["id"], "123456789")
        self.assertEqual(vacancy_info["employer_id"], "1")