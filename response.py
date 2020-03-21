import requests


def area_doctors():
    response = requests.get('https://helsi.me/api/healthy/doctors?page=1&settlement=1&speciality=сімейний%20лікар')
    if response.status_code == 200:
        data = response.json()['data']
        return [f'{item["firstName"]} {item["lastName"]}' for item in data]





def get_inf(doctor_name):
    response = requests.get(f'https://helsi.me/api/healthy/doctors?limit=30&name={doctor_name}')
    if response.status_code == 200:
        data = response.json()['data']
        try:
            name = (f"{data[0]['firstName']} {data[0]['lastName']}")
            organization = data[0]['organization']['name']
            speciality = data[0]['speciality'][0]['name']
            return [(f'{name} \n \n'
              f'Організація:\n'
              f' {organization} \n \n'
              f'Спеціалізація: \n '
              f'{speciality} \n \n')]
        except IndexError:
            return 'Wrong name'
