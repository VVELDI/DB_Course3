import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    """
    Класс для подключения к базе данных PostgreSQL и выполнения операций с ней.
    """

    def __init__(self):
        """
        Инициализация объекта DBConnection.
        Загружает параметры подключения к базе данных из переменных окружения.
        """
        self._host = os.getenv("HOST")
        self._database = os.getenv("DATABASE")
        self._username = os.getenv("USERNAME")
        self._port = os.getenv("PORT")
        self._password = os.getenv("PASSWORD")

    def connect_to_db(self, query, params=None):
        """
        Подключается к базе данных и выполняет SQL-запрос.

        :param query: SQL-запрос для выполнения.
        :param params: Параметры для SQL-запроса (опционально).
        """
        try:
            conn = psycopg2.connect(
                host=self._host,
                database=self._database,
                user=self._username,
                port=self._port,
                password=self._password,
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(query, params)
            cur.close()
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def create_db(self):
        """
        Создает новую базу данных employers_vacancy.
        Если база данных уже существует, она будет удалена и создана заново.
        """
        try:
            original_database = self._database  # Сохраняем оригинальное имя базы данных
            self._database = "postgres"  # Подключаемся к системной базе данных

            # Удаляем базу данных, если она существует
            execute_message_drop = "DROP DATABASE IF EXISTS employers_vacancy;"
            self.connect_to_db(execute_message_drop)

            # Создаем новую базу данных
            execute_message_create = "CREATE DATABASE employers_vacancy;"
            self.connect_to_db(execute_message_create)

            # Возвращаем оригинальное имя базы данных
            self._database = original_database
            print("База данных employers_vacancy успешно создана.")
        except Exception as e:
            print(f'Ошибка при создании базы данных: {e}')

    def db_clear_employers(self):
        """
        Очищает таблицу employers, удаляя все записи и сбрасывая идентификаторы.
        """
        execute_message = "TRUNCATE TABLE employers RESTART IDENTITY CASCADE;"
        self.connect_to_db(execute_message)

    def db_creating_employers(self) -> None:
        """
        Создает таблицу employers, если она не существует.

        :return: None
        """
        execute_message = """CREATE TABLE IF NOT EXISTS employers 
            (employer_id varchar PRIMARY KEY,
            company_name varchar(50) UNIQUE,
            vacancies_count int)"""
        return self.connect_to_db(execute_message)

    def db_filling_columns_for_emps(self, employers_id_list: list, employers_list: list):
        """
        Заполняет таблицу employers данными о работодателях.

        :param employers_id_list: Список идентификаторов работодателей для фильтрации.
        :param employers_list: Список словарей с данными о работодателях.
        """
        filtered_employers_list = [
            emp for emp in employers_list if emp["id"] in employers_id_list
        ]
        try:
            execute_message = """INSERT INTO employers (employer_id, company_name, vacancies_count) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (employer_id) DO NOTHING;"""  # Игнорируем дубликаты
            for employer in filtered_employers_list:
                params = (
                    employer.get("id"),
                    employer.get("name"),
                    employer.get("open_vacancies"),
                )
                self.connect_to_db(execute_message, params)
        except Exception as e:
            print(f"Ошибка: {e}")

    def db_creating_vacancies(self) -> None:
        """
        Создает таблицу vacancies, если она не существует.

        :return: None
        """
        execute_message = """CREATE TABLE IF NOT EXISTS vacancies 
            (vacancy_id varchar NOT NULL,
            vacancy_name varchar NOT NULL,
            salary_from int,
            salary_to int,
            requirement text,
            url varchar NOT NULL,
            employer_id varchar,
            FOREIGN KEY (employer_id) REFERENCES employers (employer_id))"""
        return self.connect_to_db(execute_message)

    def db_filling_vacancies(self, vacancies_list: list):
        """
        Заполняет таблицу vacancies данными о вакансиях.

        :param vacancies_list: Список словарей с данными о вакансиях.
        """
        execute_message = """INSERT INTO vacancies
                            (vacancy_id, vacancy_name, salary_from, salary_to, requirement, url, employer_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            with psycopg2.connect(
                    host=self._host,
                    database=self._database,
                    user=self._username,
                    port=self._port,
                    password=self._password,
            ) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    for vacancy in vacancies_list:
                        params = (
                            vacancy.get("id"),
                            vacancy.get("name"),
                            (
                                vacancy.get("salary").get("from")
                                if vacancy.get("salary") is not None
                                else 0
                            ),
                            (
                                vacancy.get("salary").get("to")
                                if vacancy.get("salary") is not None
                                else 0
                            ),
                            (
                                vacancy.get("snippet").get("requirement")
                                if vacancy.get("snippet") is not None
                                else ""
                            ),
                            vacancy.get("url"),
                            (
                                vacancy.get("employer").get("id")
                                if vacancy.get("employer") is not None
                                else ""
                            ),
                        )
                        try:
                            cur.execute(execute_message, params)
                        except Exception as e:
                            print(f"Ошибка при вставке вакансии: {e}")
                            print(f"Данные вакансии: {vacancy}")
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")