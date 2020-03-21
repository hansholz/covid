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
        list_of_doctors = []
        index = (len(data) - 1)
        while index !=(-1):
            try:
                name = (f"{data[index]['firstName']} {data[index]['lastName']}")
                organization = data[index]['organization']['name']
                speciality = data[index]['speciality'][0]['name']
                list_of_doctors.append((f'{name} \n \n'
                f'Організація:\n'
                f' {organization} \n \n'
                f'Спеціалізація: \n '
                f'{speciality} \n \n'))
            except IndexError:
                print( 'Wrong name')
            index -= 1
        return list_of_doctors
