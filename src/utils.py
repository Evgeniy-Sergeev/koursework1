from src.api import HeadHunterAPI
from src.storage import JSONSaver
from src.vacancy import Vacancy


def parse_salary(salary: dict or str) -> int:
    """
    Функция для парсинга зарплаты. Возвращает минимальное значение зарплаты как целое число.

    :param salary: Может быть строкой с зарплатой (например, '100 000-150 000 руб.')
                   или словарем с полями 'from' и 'to' (например, {'from': 100000, 'to': 150000}).
                   Может быть None, если зарплата не указана.
    :return: Минимальное значение зарплаты как целое число. Если зарплата не указана, возвращает 0.
    """
    if salary is None:
        return 0  # Если зарплата отсутствует (None), возвращаем 0

    if isinstance(salary, dict):
        # Если зарплата предоставлена в виде словаря
        return salary.get('from', 0)  # Возвращаем минимальную зарплату (если есть), иначе 0

    elif isinstance(salary, str):
        # Если зарплата предоставлена в виде строки
        if salary == 'Зарплата не указана':
            return 0
        salary_range = salary.replace(' ', '').split('-')
        try:
            return int(salary_range[0].replace('руб.', ''))
        except ValueError:
            return 0

    return 0  # Если формат зарплаты неизвестен, возвращаем 0


def get_salary_input() -> int:
    """
    Функция для ввода желаемой зарплаты от пользователя.

    :return: Значение зарплаты как целое число.
    """
    while True:
        try:
            salary = int(input("Введите желаемую зарплату (в рублях): "))
            if salary < 0:
                print("Зарплата не может быть отрицательной. Пожалуйста, введите корректное значение.")
                continue
            return salary
        except ValueError:
            print("Пожалуйста, введите корректное число.")


def get_top_vacancies(vacancies: list, salary: int) -> list:
    """
    Фильтрация вакансий по зарплате и вывод всех вакансий с зарплатой выше указанной.

    :param vacancies: Список вакансий.
    :param salary: Минимальная желаемая зарплата.
    :return: Список всех вакансий, соответствующих критерию.
    """
    # Фильтрация вакансий по зарплате, если зарплата не None
    filtered_vacancies = [v for v in vacancies if parse_salary(v.get('salary')) >= salary]

    # Сортировка вакансий по убыванию зарплаты
    sorted_vacancies = sorted(filtered_vacancies, key=lambda v: parse_salary(v.get('salary')), reverse=True)

    return sorted_vacancies  # Возвращаем все вакансии, соответствующие критерию


def search_vacancies_by_keyword(vacancies: list, keyword: str) -> list:
    """
    Поиск вакансий по ключевому слову в описании.

    :param vacancies: Список вакансий.
    :param keyword: Ключевое слово для поиска.
    :return: Список вакансий, содержащих ключевое слово.
    """
    if not keyword:
        print("Ошибка: ключевое слово не должно быть пустым.")
        return []

    found_vacancies = [v for v in vacancies if 'description' in v and keyword.lower() in v['description'].lower()]
    return found_vacancies


def user_interaction():
    """
    Функция для взаимодействия с пользователем через терминал.
    """
    try:
        hh_api = HeadHunterAPI()
        json_saver = JSONSaver('vacancies.json')

        # Получаем запрос пользователя
        search_query = input("Введите поисковый запрос для вакансий (например, 'Python разработчик'): ")
        if not search_query:
            print("Ошибка: поисковый запрос не должен быть пустым.")
            return

        # Получаем вакансии с hh.ru
        hh_vacancies = hh_api.get_vacancies(search_query)
        if not hh_vacancies:
            print("Вакансий по данному запросу не найдено.")
            return

        # Преобразуем данные API в объекты Vacancy и добавляем их в JSON файл
        vacancy_objects = [
            Vacancy(v['name'], v['alternate_url'], v['salary'], v['snippet']['responsibility'])
            for v in hh_vacancies
        ]
        for vacancy in vacancy_objects:
            json_saver.add_vacancy(vacancy)

        # Ввод желаемой зарплаты
        salary = get_salary_input()

        # Получаем вакансии из файла и фильтруем по зарплате
        saved_vacancies = json_saver.get_vacancies()
        top_vacancies = get_top_vacancies(saved_vacancies, salary)

        # Выводим все подходящие вакансии
        print(f"\nВакансии с зарплатой от {salary} руб:")
        if top_vacancies:
            for i, vacancy in enumerate(top_vacancies, 1):
                print(f"{i}. {vacancy['title']} ({vacancy['salary']}) - {vacancy['url']}")
        else:
            print("Нет вакансий, соответствующих указанной зарплате.")

        # Поиск по ключевому слову
        keyword = input("\nВведите ключевое слово для поиска вакансий в описании: ")
        if not keyword:
            print("Ошибка: ключевое слово не должно быть пустым.")
            return

        found_vacancies = search_vacancies_by_keyword(saved_vacancies, keyword)

        # Выводим найденные вакансии
        if found_vacancies:
            print(f"\nВакансии, содержащие '{keyword}' в описании:")
            for i, vacancy in enumerate(found_vacancies, 1):
                print(f"{i}. {vacancy['title']} ({vacancy['salary']}) - {vacancy['url']}")
        else:
            print(f"\nВакансий с ключевым словом '{keyword}' не найдено.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def search_vacancies_by_keyword(vacancies, keyword):
    found_vacancies = [
        v for v in vacancies
        if 'description' in v and v['description'] is not None and keyword.lower() in v['description'].lower()
    ]
    return found_vacancies


if __name__ == "__main__":
    user_interaction()
