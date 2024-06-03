from src.hh_api import HH_api
from src.DB_Manager import DBManager
hh_api = HH_api()

def main():

    # Создаем экземпляр класса DBManager
    db_manager = DBManager()

    # Вызываем методы для работы с базой данных и заполняем ее
    db_manager.create_database()
    db_manager.create_tables()
    employers_info = hh_api.get_employers_info()
    vacancies_details = hh_api.get_vacancies_details()
    db_manager.save_info_db(employers_info, vacancies_details)

    print("Список компаний и количество вакансий в компаниях:")
    rows = db_manager.get_companies_and_vacancies_count()
    for row in rows:
        print(f'{row[0]} - {row[1]}')

    print("Список вакансий их зп и ссылки")
    rows = db_manager.get_all_vacancies()
    for row in rows[:3]:
        employer_name, vacancy_name, salary_from, salary_to, url = row
        if salary_to is None and salary_from is None:
            print(f'{employer_name} - {vacancy_name} - Зарплата не указана - {url}')
        elif salary_to is None:
            print(f'{employer_name} - {vacancy_name} - Зарплата от {salary_from} - {url}')
        elif salary_from is None:
            print(f'{employer_name} - {vacancy_name} - Зарплата до {salary_to} - {url}')
        else:
            print(f'{employer_name} - {vacancy_name} - Зарплата от {salary_from} до {salary_to} - {url}')

    print("Средняя зарплата по компаниям:")
    rows = db_manager.get_avg_salary()
    for row in rows:
        print(f'{row[0]} - {row[1]}')

    print("список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    rows = db_manager.get_all_vacancies()
    for row in rows[:3]:
        print(row[1])

    print("список всех вакансий, в названии которых содержатся переданные в метод слова, например python")
    user_input = input("или выберите сами, можно пропустить ввести  'skip': ")
    if user_input == 'skip':
        pass
    else:
        rows = db_manager.get_vacancies_with_keyword(user_input)
        for row in rows[:3]:
            print(row)


if __name__ == '__main__':
    main()
