import psycopg2
from src.DB_Create_module import DBConnection


class DBManager(DBConnection):
    """
    Класс для взаимодействия с базой данных.
    Наследует функциональность от DBConnection и добавляет методы для получения данных из базы.
    """

    def __init__(self):
        """
        Инициализация объекта DBManager.
        Вызывает конструктор родительского класса DBConnection.
        """
        super().__init__()

    def connect_to_db(self, query, params=None):
        """
        Подключается к базе данных, выполняет SQL-запрос и возвращает результат.

        :param query: SQL-запрос для выполнения.
        :param params: Параметры для SQL-запроса (опционально).
        :return: Результат выполнения запроса или пустой список в случае ошибки.
        """
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
                    cur.execute(query, params)
                    result = cur.fetchall()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            result = []
        return result

    def get_companies_and_vacancies_count(self):
        """
        Получает список компаний и количество вакансий у каждой компании.

        :return: Строка с названиями компаний и количеством их вакансий.
        """
        execute_message = """SELECT employers.company_name, COUNT(vacancies.employer_id)
        FROM employers JOIN vacancies USING (employer_id) GROUP BY employer_id"""
        return f'Компании и количество вакансий:\n{self.connect_to_db(execute_message)}'

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с информацией о компании, названии вакансии, зарплате и ссылке.

        :return: Строка с информацией о вакансиях.
        """
        execute_message = """SELECT employers.company_name, vacancies.vacancy_name, 
        ((vacancies.salary_from + vacancies.salary_to) / 2), vacancies.url
        FROM vacancies JOIN employers USING(employer_id)"""
        return f'Список всех вакансий:\n{self.connect_to_db(execute_message)[:10]} \n ...'

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по всем вакансиям.

        :return: Строка с информацией о средней зарплате.
        """
        execute_message = """SELECT AVG((vacancies.salary_from + vacancies.salary_to) / 2) FROM vacancies"""
        return f'Средняя зарплата по вакансиям:\n{self.connect_to_db(execute_message)}'

    def get_vacancies_with_higher_salary(self):
        """
        Получает список вакансий с зарплатой выше средней.

        :return: Строка с информацией о вакансиях с зарплатой выше средней.
        """
        execute_message = """SELECT * FROM vacancies WHERE ((vacancies.salary_from + vacancies.salary_to) / 2) > 
(SELECT (AVG((vacancies.salary_from + vacancies.salary_to) / 2)) FROM vacancies)"""
        return f'Вакансии с зарплатой выше среднего:\n{self.connect_to_db(execute_message)[:10]}'

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список вакансий, содержащих ключевое слово в названии.

        :param keyword: Ключевое слово для поиска в названиях вакансий.
        :return: Строка с информацией о вакансиях, содержащих ключевое слово.
        """
        execute_message = f"""SELECT * FROM vacancies WHERE vacancy_name ILIKE '%{keyword}%'"""
        return f'Вакансии по ключевому слову:\n{self.connect_to_db(execute_message)[:10]}'