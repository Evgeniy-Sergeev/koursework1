from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.storage import JSONSaver
from src.utils import search_vacancies_by_keyword


def user_interaction():
    search_query = input("Введите поисковый запрос для вакансий (например, 'Python разработчик'): ")
    if not search_query.strip():
        print("Ошибка: поисковый запрос не должен быть пустым.")
        return

    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        print("Ошибка: необходимо ввести число для топ N.")
        return

    filter_words = input("Введите ключевые слова для фильтрации вакансий(например, удаленная работа): ").split()
    salary_range = input("Введите диапазон зарплат (например, 100000-150000): ").split('-')
    min_salary = int(salary_range[0].strip()) if salary_range[0].strip().isdigit() else None
    max_salary = int(salary_range[1].strip()) if len(salary_range) > 1 and salary_range[1].strip().isdigit() else None

    hh_api = HeadHunterAPI()
    json_file_path = 'vacancies.json'
    json_saver = JSONSaver(json_file_path)

    hh_vacancies = hh_api.get_vacancies(search_query)
    if not hh_vacancies:
        print("Вакансий по данному запросу не найдено.")
        return

    vacancy_objects = [
        Vacancy(v.get('name', 'Не указано'), v.get('alternate_url', '#'), v.get('salary', 'Зарплата не указана'),
                v['snippet'].get('responsibility', 'Описание не указано'))
        for v in hh_vacancies
    ]
    for vacancy in vacancy_objects:
        json_saver.add_vacancy(vacancy)

    saved_vacancies = json_saver.get_vacancies()

    filtered_vacancies = [
        v for v in saved_vacancies
        if (
                   (isinstance(v.get('salary'), dict) and (
                           (min_salary is None or (
                                   v['salary'].get('from') is not None and v['salary']['from'] >= min_salary)) and
                           (max_salary is None or (
                                   v['salary'].get('to') is not None and v['salary']['to'] <= max_salary))
                   )) or v.get('salary') == 'Зарплата не указана') and all(
            word.lower() in v.get('description', '').lower() for word in filter_words)
    ]

    filtered_with_salary = [
        v for v in filtered_vacancies if isinstance(v.get('salary'), dict) and v['salary'].get('from') is not None
    ]
    filtered_without_salary = [v for v in filtered_vacancies if v.get('salary') == 'Зарплата не указана']
    top_vacancies = sorted(filtered_with_salary, key=lambda x: x['salary'].get('from', 0), reverse=True)[:top_n] + \
                    filtered_without_salary[:max(0, top_n - len(filtered_with_salary))]
    print(f"\nТоп {top_n} вакансий по запросу '{search_query}':")
    if top_vacancies:
        for i, vacancy in enumerate(top_vacancies, 1):
            if isinstance(vacancy.get('salary'), dict) and vacancy['salary'].get('from') is not None:
                salary = f"{vacancy['salary'].get('from', 0)} - {vacancy['salary'].get('to', 'не указано')}"
                print(f"{i}. {vacancy.title} ({salary}) - {vacancy.url}")  # Добавьте vacancy.title и vacancy.url
            else:
                print(f"{i}. {vacancy.title} - {vacancy.url}")  # Добавьте vacancy.title и vacancy.url
    else:
        print("Нет вакансий, соответствующих указанным критериям.")

    keyword = input("\nВведите ключевое слово для поиска вакансий в описании: ")
    if not keyword.strip():
        print("Ошибка: ключевое слово не должно быть пустым.")
        return

    found_vacancies = search_vacancies_by_keyword(saved_vacancies, keyword)

    if found_vacancies:
        print(f"\nВакансии, содержащие '{keyword}' в описании:")
        for i, vacancy in enumerate(found_vacancies, 1):
            if isinstance(vacancy.get('salary'), dict) and vacancy['salary'].get('from') is not None:
                salary = f"{vacancy['salary'].get('from', 0)} - {vacancy['salary'].get('to', 'не указано')}"
                print(f"{i}. {vacancy.title} ({salary}) - {vacancy.url}")  # Добавьте vacancy.title и vacancy.url
            else:
                print(f"{i}. {vacancy.title} - {vacancy.url}")  # Добавьте vacancy.title и vacancy.url
    else:
        print(f"\nВакансий с ключевым словом '{keyword}' не найдено.")
    print("Работа программы завершена.")


if __name__ == "main":
    user_interaction()
