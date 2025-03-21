import json
import os
from abc import ABC, abstractmethod

from src.vacancy import Vacancy


class SaverABC(ABC):
    """
    Абстрактный базовый класс для работы с сохранением, добавлением и удалением вакансий.
    Определяет обязательные методы для работы с вакансиями.
    """

    @abstractmethod
    def save_to_json_file(self, vac_obj_list):
        """
        Абстрактный метод для сохранения списка вакансий в файл.

        :param vac_obj_list: Список объектов вакансий для сохранения.
        """
        pass

    @abstractmethod
    def add_vacancy(self, vacancy_object):
        """
        Абстрактный метод для добавления вакансии в файл.

        :param vacancy_object: Объект вакансии для добавления.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_object):
        """
        Абстрактный метод для удаления вакансии из файла.

        :param vacancy_object: Объект вакансии для удаления.
        """
        pass


class JSONSaver(SaverABC):
    """
    Класс для сохранения списка объектов в файл, добавления и удаления объектов.
    Реализует методы для работы с JSON-файлом.
    """

    def __init__(self):
        """
        Инициализация объекта JSONSaver.
        Устанавливает путь к файлу для сохранения вакансий.
        """
        self.path = os.path.join(os.getcwd(), "data/vacancies.json")

    def save_to_json_file(self, vac_obj_list):
        """
        Сохраняет список объектов вакансий в JSON-файл.

        :param vac_obj_list: Список объектов вакансий для сохранения.
        """
        vac_dicts_list = [vacancy.get_vacancy_info for vacancy in vac_obj_list]
        with open(self.path, mode="w") as json_file:
            json.dump(vac_dicts_list, json_file, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy_object: Vacancy):
        """
        Добавляет вакансию в JSON-файл, если её ещё нет в файле.

        :param vacancy_object: Объект вакансии для добавления.
        :return: Сообщение о результате операции.
        """
        vac_to_add = vacancy_object.get_vacancy_info
        with open(self.path, mode="r+") as json_file:
            py_file = json.load(json_file)
            if not vac_to_add.get("id") in [vacancy.get("id") for vacancy in py_file]:
                py_file.append(vac_to_add)
                json_file.seek(0)
                json_file.truncate()
                json.dump(py_file, json_file, indent=4, ensure_ascii=False)
            else:
                return "Vacancy already in data"

    def delete_vacancy(self, vacancy_object: Vacancy):
        """
        Удаляет вакансию из JSON-файла, если она существует.

        :param vacancy_object: Объект вакансии для удаления.
        :return: Сообщение о результате операции.
        """
        vac_to_del = vacancy_object.get_vacancy_info
        with open(self.path, mode="r+") as json_file:
            py_file = json.load(json_file)
            for vacancy in py_file:
                if vac_to_del.get("id") == vacancy.get("id"):
                    py_file.remove(vacancy)
                    json_file.seek(0)
                    json_file.truncate()
                    json.dump(py_file, json_file, indent=4, ensure_ascii=False)
                    return "Vacancy deleted successfully"
        return "Vacancy is not in data"