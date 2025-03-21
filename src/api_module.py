from abc import ABC, abstractmethod
import requests
import time


class ApiHH(ABC):
    """
    Абстрактный базовый класс для работы с API HeadHunter.
    Определяет обязательный метод инициализации.
    """

    @abstractmethod
    def __init__(self):
        """
        Абстрактный метод инициализации.
        """
        pass


class FindVacancyFromHHApi(ApiHH):
    """
    Класс для получения данных по вакансиям из API HeadHunter.
    """

    def __init__(self):
        """
        Инициализация объекта FindVacancyFromHHApi.
        Устанавливает URL, заголовки и параметры для запросов к API.
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def __get_vacancies(self, keyword: str):
        """
        Приватный метод для получения списка вакансий по ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        """
        self.__params["text"] = keyword
        try:
            while self.__params.get("page") != 20:
                if (
                    requests.get(
                        self.__url, headers=self.__headers, params=self.__params
                    ).status_code
                    == 200
                ):
                    response = requests.get(
                        self.__url, headers=self.__headers, params=self.__params
                    )
                    vacancies = response.json()["items"]
                    self.__vacancies.extend(vacancies)
                    self.__params["page"] += 1
        except Exception as e:
            print(f"Что-то не так с подключением, ошибка: {e}")

    def __get_vacancies_by_employer_id(self, employer_id: str):
        """
        Приватный метод для получения вакансий по идентификационному номеру работодателя.

        :param employer_id: Идентификационный номер работодателя.
        """
        try:
            self.__params["employer_id"] = employer_id
            while self.__params.get("page") != 10:
                response = requests.get(
                    self.__url, headers=self.__headers, params=self.__params
                )
                response_data = response.json()

                if "items" in response_data:
                    vacancies = response_data["items"]
                    self.__vacancies.extend(vacancies)
                else:
                    print(f"Нет вакансий для работодателя с ID: {employer_id}")
                    break  # Выход из цикла, если нет вакансий

                self.__params["page"] += 1
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def get_vacancies(self, keyword: str) -> list:
        """
        Получает список вакансий в формате JSON из приватного метода __get_vacancies.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список вакансий.
        """
        self.__get_vacancies(keyword)
        return self.__vacancies

    def get_vacancies_by_employer_id(self, employer_id: str) -> list:
        """
        Получает список вакансий по идентификационному номеру работодателя.

        :param employer_id: Идентификационный номер работодателя.
        :return: Список вакансий.
        """
        self.__get_vacancies_by_employer_id(employer_id)
        return self.__vacancies


class FindEmployerFromHHApi(ApiHH):
    """
    Класс для получения данных о работодателях из API HeadHunter.
    """

    def __init__(self):
        """
        Инициализация объекта FindEmployerFromHHApi.
        Устанавливает URL, заголовки и параметры для запросов к API.
        """
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "sort_by": "by_vacancies_open",
        }
        self.__employers = []

    def __get_employer_info(self, keyword=""):
        """
        Приватный метод для получения информации о работодателях из API HeadHunter.

        :param keyword: Ключевое слово для поиска работодателей.
        """
        try:
            self.__params["text"] = keyword
            while self.__params.get("page") != 20:
                response = requests.get(
                    self.__url, headers=self.__headers, params=self.__params
                )
                employers = response.json()
                self.__employers.extend(employers["items"])
                self.__params["page"] += 1
        except Exception as e:
            print(f"Что-то не так с подключением, ошибка: {e}")

    def get_employer_info(self, employers_count, keyword="") -> list:
        """
        Получает информацию о работодателях и выводит её на экран.

        :param employers_count: Количество работодателей для вывода.
        :param keyword: Ключевое слово для поиска работодателей.
        :return: Список работодателей.
        """
        self.__get_employer_info(keyword)
        for employer in self.__employers[:employers_count]:
            print(f"{employer.get('name')}, id: {employer.get('id')}")
        print("...")
        return self.__employers