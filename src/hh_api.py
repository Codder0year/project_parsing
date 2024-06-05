import requests

class HH_api:
    def __init__(self):
        self.base_url = 'https://api.hh.ru'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.employers = [
            'ООО Итсен',
            'Amex Development',
            'Тинькофф',
            'Inline Telecom Solutions',
            'KTS',
            'ООО Интем Лаб',
            'Первый Бит',
            '7RedLines',
            'Aiti Guru'
        ]

    def get_employers_info(self) -> list:
        """Получение информации о работодателях"""
        employers_info = []
        for employer_name in self.employers:
            params = {'text': employer_name, 'sort_by': 'by_name', 'page': 0, 'per_page': 1}
            response = requests.get(f"{self.base_url}/employers", headers=self.headers, params=params)

            if response.status_code == 200:
                data = response.json()
                if data['found'] > 0:
                    employer_id = data['items'][0]['id']
                    employer_name = data['items'][0]['name']
                    open_vacancies = data['items'][0]['open_vacancies']

                    # Получаем полную информацию о работодателе
                    employer_response = requests.get(f"{self.base_url}/employers/{employer_id}", headers=self.headers)
                    if employer_response.status_code == 200:
                        employer_data = employer_response.json()
                        description = employer_data.get('description', 'Нет описания')

                        employer_info = {
                            'employer_id': employer_id,
                            'employer_name': employer_name,
                            'open_vacancies': open_vacancies,
                            'description': description
                        }
                        employers_info.append(employer_info)
                    else:
                        print(f"Не удалось получить полную информацию для работодателя с ID: {employer_id}")
                else:
                    print(f"Работодатель с именем: {employer_name} не найден")
            else:
                print(f"Не удалось получить данные для работодателя: {employer_name}")

        return employers_info

    def get_vacancies(self, employer_id) -> list:
        """Получение списка вакансий для конкретного работодателя"""
        params = {
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True,
            "per_page": 100,
            "page": 0
        }
        response = requests.get(f"{self.base_url}/vacancies", headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            print(f"Не удалось получить вакансии для работодателя с ID: {employer_id}")
            return []

    def get_vacancies_details(self) -> list:
        """Получение деталей по всем вакансиям всех работодателей"""
        employers = self.get_employers_info()
        vacancies_list = []
        for employer in employers:
            employer_id = employer['employer_id']
            employer_name = employer['employer_name']
            vacancies = self.get_vacancies(employer_id)
            for vacancy in vacancies:
                vacancy_details = {
                    'employer_id': employer_id,
                    'employer_name': employer_name,
                    'vacancy_id': vacancy['id'],
                    'vacancy_name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'salary_from': vacancy['salary']['from'],
                    'salary_to': vacancy['salary']['to'],
                    'description': vacancy.get('snippet', {}).get('responsibility', 'Описание отсутствует')
                }
                vacancies_list.append(vacancy_details)
        return vacancies_list
