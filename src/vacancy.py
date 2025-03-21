from abc import ABC, abstractmethod


class VacancyABC(ABC):
    """
    Абстрактный базовый класс для работы с вакансиями.
    Определяет обязательный метод для преобразования JSON-данных в список объектов.
    """

    @abstractmethod
    def cast_to_object_list(self, json_vacancies):
        """
        Абстрактный метод для преобразования JSON-данных в список объектов.

        :param json_vacancies: Список вакансий в формате JSON.
        :return: Список объектов вакансий.
        """
        pass


class Vacancy(VacancyABC):
    """
    Класс для представления вакансии.

    Использует слоты для оптимизации памяти и хранения данных о вакансии.
    Реализует метод для преобразования JSON-данных в список объектов.
    """

    __slots__ = (
        "__vacancy_name",
        "__vacancy_url",
        "__salary_from",
        "__salary_to",
        "__requirement",
        "__id",
        "__employer_id",
    )

    def __init__(
        self,
        vacancy_name,
        vacancy_url,
        salary_from,
        salary_to,
        requirement,
        vacancy_id,
        employer_id,
    ):
        """
        Инициализация объекта Vacancy.

        :param vacancy_name: Название вакансии.
        :param vacancy_url: Ссылка на вакансию.
        :param salary_from: Нижняя граница зарплаты.
        :param salary_to: Верхняя граница зарплаты.
        :param requirement: Требования к вакансии.
        :param vacancy_id: Уникальный идентификатор вакансии (должен состоять из 9 символов).
        :param employer_id: Уникальный идентификатор работодателя.
        """
        self.__vacancy_name: str = vacancy_name
        self.__vacancy_url: str = vacancy_url if vacancy_url else "Ссылка не указана"
        self.__salary_from: int = salary_from if salary_from else 0
        self.__salary_to: int = salary_to if salary_to else 0
        self.__requirement: str = (
            requirement if requirement else "Требования не указаны"
        )
        self.__id: str = vacancy_id if len(vacancy_id) == 9 else "Unknown"
        self.__employer_id: str = employer_id

    @classmethod
    def cast_to_object_list(cls, json_vacancies) -> list:
        """
        Классовый метод для преобразования списка словарей (вакансий) в формате JSON,
        полученного от API HH.ru, в список объектов Vacancy.

        :param json_vacancies: Список вакансий в формате JSON.
        :return: Список объектов Vacancy.
        """
        vacancies_list = []
        for vacancy in json_vacancies:
            vacancy_new = cls(
                vacancy.get("name"),
                vacancy.get("alternate_url"),
                (
                    vacancy.get("salary", {}).get("from")
                    if vacancy.get("salary") is not None
                    else 0
                ),
                (
                    vacancy.get("salary", {}).get("to")
                    if vacancy.get("salary") is not None
                    else 0
                ),
                vacancy.get("snippet").get("requirement"),
                vacancy.get("id"),
                vacancy.get("employer").get("id"),
            )
            vacancies_list.append(vacancy_new)
        return vacancies_list

    @property
    def get_vacancy_info(self) -> dict:
        """
        Геттер для получения информации о вакансии в виде словаря.

        :return: Словарь с информацией о вакансии.
        """
        vacancy_dict = {
            "name": self.__vacancy_name,
            "url": self.__vacancy_url,
            "salary_from": self.__salary_from,
            "salary_to": self.__salary_to,
            "requirement": self.__requirement,
            "id": self.__id,
            "employer_id": self.__employer_id,
        }
        return vacancy_dict