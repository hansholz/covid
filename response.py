import requests


def kyiv_doctors():
    response = requests.get('https://helsi.me/api/healthy/doctors?page=1&settlement=1&speciality=сімейний%20лікар')
    if response.status_code == 200:
        data = response.json()['data']
        return [f'{item["firstName"]} {item["lastName"]}' for item in data]
