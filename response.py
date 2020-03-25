import requests
import sqlite3


def doctors_from_specialty(speciality, city_id):
    response = requests.get(f'https://helsi.me/api/healthy/doctors?settlement={city_id}&speciality={speciality}')
    if response.status_code == 200:
        data = response.json()['data']
        list_of_doctors = []
        index = (len(data) - 1)
        while index != (-1):
            name = (f"{data[index]['firstName']} {data[index]['lastName']}")
            list_of_doctors.append(name)
            index -= 1
        return list_of_doctors


def search_of_city(city_name):
    response = requests.get(f'https://helsi.me/api/addressservice/settlements?search={city_name}')
    if response.status_code == 200:
        data = response.json()
        list_of_cities = []
        index = (len(data) - 1)

        conn = sqlite3.connect('regions.sqlite3')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ident_city (city_name TEXT NOT NULL, city_id INTEGER NOT NULL)')

        while index != (-1):
            city_name = data[index]['name']
            region = data[index]['region']
            city_id = data[index]['id']

            c.execute(f'INSERT INTO ident_city (city_name, city_id) SELECT "{city_name}", "{city_id}" WHERE NOT EXISTS(SELECT 1 FROM ident_city WHERE city_name = "{city_name}" AND city_id = "{city_id}");')
            conn.commit()

            list_of_cities.insert(0, f'{city_name}')
            index -= 1
        return list_of_cities


def get_inf(doctor_name):
    response = requests.get(f'https://helsi.me/api/healthy/doctors?limit=30&name={doctor_name}')
    if response.status_code == 200:
        data = response.json()['data']
        list_of_doctors = []
        index = (len(data) - 1)
        while index !=(-1):
            try:
                resource_id = data[index]['resourceId']
                response_resource_id = requests.get(f'https://helsi.me/api/healthy/doctors/{resource_id}')
                if response_resource_id.status_code == 200:
                    id_data = response_resource_id.json()
                name = (f"{data[index]['firstName']} {data[index]['lastName']}")
                organization = data[index]['organization']['name']
                speciality = data[index]['speciality'][0]['name']
                address = data[index]['organization']['addresses']['address']['addressText']
                phone = id_data['contactPhones'][0]

                list_of_doctors.append((f'{name} \n \n'
                f'Організація:\n'
                f' {organization} \n '
                f'{address} \n \n'
                f'Спеціалізація: \n '
                f'{speciality} \n \n'
                f'Робочий телефон: \n '
                f'{phone} \n \n'))
            except IndexError:
                print('Wrong name')
            index -= 1
        return list_of_doctors
