import requests


def kyiv_doctors():
    response = requests.get('https://helsi.me/api/healthy/doctors?page=1&settlement=1&speciality=сімейний%20лікар')
    if response.status_code == 200:
        data = response.json()['data']
        return [f'{item["firstName"]} {item["lastName"]}' for item in data]


doctors = kyiv_doctors()


def get_inf():
    doctor_name = doctors[10]
    response = requests.get(f'https://helsi.me/api/healthy/doctors?limit=30&name={doctor_name}&settlement=1')
    if response.status_code == 200:
        data = response.json()['data']
        organization = data[0]['organization']['name']
        speciality = data[0]['speciality'][0]['name']
        return [(f'{doctor_name} \n'
              f'Організація:\n'
              f' {organization} \n'
              f'Спеціалізація: \n '
              f'{speciality}')]


get_inf()