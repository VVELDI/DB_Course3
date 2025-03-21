import re


def filter_vacancies(vacs_obj_list: list, filter_words) -> list:
    """
    Фильтрует список вакансий по ключевым словам в требованиях.

    :param vacs_obj_list: Список объектов вакансий.
    :param filter_words: Список ключевых слов для фильтрации.
    :return: Отфильтрованный список вакансий.
    """
    filtered_vacancies = []
    for vacancy in vacs_obj_list:
        for word in filter_words:
            match = re.search(word, vacancy.get_vacancy_info.get("requirement"))
            if match:
                filtered_vacancies.append(vacancy)
                break
    return filtered_vacancies


def get_top_vacancies(srtd_vacancies, top_n) -> str:
    """
    Возвращает топ-N вакансий из отсортированного списка.

    :param srtd_vacancies: Отсортированный список вакансий.
    :param top_n: Количество вакансий для вывода.
    :return: Строка с информацией о топ-N вакансиях.
    """
    top_n_vacancies = srtd_vacancies[:top_n]
    result = ""
    for vacancy in top_n_vacancies:
        result += f"""Вакансия: {vacancy.get('name')}
        Зарплата от {vacancy.get('salary_from')} до {vacancy.get('salary_to')}
        Требования: {vacancy.get('requirement')}
        Ссылка: {vacancy.get('url')}
        \n"""
    return result


def sort_vacancies(ranged_by_salary_vacs_list) -> list:
    """
    Сортирует список вакансий по средней зарплате (по убыванию).

    :param ranged_by_salary_vacs_list: Список вакансий, отфильтрованных по зарплате.
    :return: Отсортированный список вакансий.
    """
    vacs_list = [vacancy.get_vacancy_info for vacancy in ranged_by_salary_vacs_list]
    sorted_vacs_list = sorted(
        vacs_list,
        key=lambda vac: vac.get("salary_from", 0) + vac.get("salary_to", 0),
        reverse=True,
    )
    return sorted_vacs_list


def get_vacancies_by_salary(fltrd_list, salary_from, salary_to) -> list:
    """
    Фильтрует список вакансий по диапазону зарплат.

    :param fltrd_list: Список вакансий, отфильтрованных по ключевым словам.
    :param salary_from: Нижняя граница зарплаты.
    :param salary_to: Верхняя граница зарплаты.
    :return: Список вакансий, попадающих в указанный диапазон зарплат.
    """
    ranged_vacancies = []
    for vacancy in fltrd_list:
        sal_from = int(vacancy.get_vacancy_info.get("salary_from"))
        sal_to = int(vacancy.get_vacancy_info.get("salary_to"))
        avg_salary = (sal_from + sal_to) / len([sal_from, sal_to])
        if int(salary_from) < int(avg_salary) < int(salary_to):
            ranged_vacancies.append(vacancy)
    return ranged_vacancies