import requests


def specialty():
    response = requests.get('https://helsi.me/api/healthy/specialities')
    if response.status_code == 200:
        data = response.json()
        list = []
        for name in data:
            list.append(name['name'])
        return list


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

