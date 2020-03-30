import telebot
from telebot import types
import sqlite3
from response import get_inf
from response import search_of_city
from response import doctors_from_specialty


with open("token.txt") as f:
    token = f.read().strip()
TOKEN = f'{token}'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hi, man. Do you want /choose_doctor ?')


@bot.message_handler(commands=['choose_doctor'])
def choose_doctor(message):
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text=f"За прізвищем", callback_data=f"w_fn_ls")
    itembtn2 = types.InlineKeyboardButton(text=f"За спеціальністю", callback_data=f"w_s")
    key.add(itembtn)
    key.add(itembtn2)
    bot.send_message(message.chat.id, f'Яким чином ви хочете знайти лікаря?', reply_markup=key)


@bot.message_handler(content_types=['city'])
def search_with_alph(message):
    quest_msg = bot.send_message(message.chat.id, f'Введіть назву міста, в якому ви хочете знайти лікаря:')
    bot.register_next_step_handler(quest_msg, identify_city)


def identify_city(message):
    if message.text == '/choose_doctor':
        choose_doctor(message)
    else:
        key = types.InlineKeyboardMarkup()
        data = search_of_city(message.text)

        if len(data) < 1:
            bot.send_message(message.chat.id, f'За вашим запитом нічого не знайдено :( \nПовторіть спробу')
            search_with_alph(message)
        else:
            for city in data:

                conn = sqlite3.connect('regions.sqlite3')
                c = conn.cursor()
                city_name = (city[:(city.index(" "))])
                region_name = city[((city.index("("))+1):-1]
                c.execute(f'SELECT city_id FROM ident_city WHERE city_name = "{city_name.replace("_", " ")}" AND region_name = "{region_name}";')
                city_id = list(c)

                itembtn = types.InlineKeyboardButton(text=f"{city.replace('_', ' ')}", callback_data=f"{city_id[0][0]}")
                key.add(itembtn)
            bot.send_message(message.chat.id, f'Міста за запитом: "{message.text}" \nОберіть необхідне ', reply_markup=key)


@bot.message_handler(content_types=['first_symbol'])
def enter_first_symbol(message):
    quest_msg = bot.send_message(message.chat.id, f'Введіть першу букву назви спеціальності:')
    bot.register_next_step_handler(quest_msg, get_inf_specialty)


def get_inf_specialty(message):
    if message.text == '/choose_doctor':
        choose_doctor(message)
    else:
        key = types.InlineKeyboardMarkup()
        if len(message.text) > 1:
            bot.send_message(message.chat.id, f'Введіть тільки одну букву')
            enter_first_symbol(message)
        else:
            conn = sqlite3.connect('regions.sqlite3')
            c = conn.cursor()
            c.execute('SELECT * FROM specialty')

            data = list(c)
            first = str(message.text).strip().lower()
            alph = ('а б в г д е є ж з и і ї й к л м н о п р с т у х ч щ ю я').split(' ')
            if first in alph:
                for spclty in data:
                    if str(spclty[1])[0].lower() == first:
                        itembtn = types.InlineKeyboardButton(text=f"{spclty[1]}", callback_data=f"{spclty[1].replace(' ', '_')}")
                        key.add(itembtn)
            bot.send_message(message.chat.id, f'Спеціальності на букву: {message.text}', reply_markup=key)


def doctors_in_area(message):
    key = types.InlineKeyboardMarkup()

    conn = sqlite3.connect('regions.sqlite3')
    c = conn.cursor()
    c.execute(f'SELECT city FROM session WHERE user_id = {message.chat.id};')
    city_id = list(c)[0][0]
    c.execute(f'SELECT speciality FROM session WHERE user_id = {message.chat.id};')
    speciality = list(c)[0][0]
    c.execute(f'SELECT city_name FROM ident_city WHERE city_id = "{city_id}";')
    city_name = list(c)[0][0]

    data = doctors_from_specialty(speciality, city_id)
    if len(data) < 1:
        bot.send_message(message.chat.id, f'За вашим запитом нічого не знайдено :( \nПовторіть спробу настиснувши /choose_doctor')

    if len(data) > 1:
        for doctor in data:
            inform = doctor.rsplit(' ')

            c.execute('CREATE TABLE IF NOT EXISTS doctors (doctor TEXT NOT NULL)')
            c.execute(f'INSERT INTO doctors (doctor) SELECT "{inform[0]} {inform[1]}" WHERE NOT EXISTS(SELECT 1 FROM doctors WHERE doctor = "{inform[0]} {inform[1]}");')
            conn.commit()

            itembtn = types.InlineKeyboardButton(text=f"{inform[0]} {inform[1]}", callback_data=f"{inform[0]}_{inform[1]}")
            key.add(itembtn)
        bot.send_message(message.chat.id, f'Лікарі в місті {city_name} за спеціальністю {speciality}:', reply_markup=key)
    else:
        bot.reply_to(message, doctors_from_specialty(message.text, city_id))


@bot.message_handler(content_types=['text'])
def information_about_doctors(message):
    quest_msg = bot.send_message(message.chat.id, f'Введіть прізвище лікаря:')
    bot.register_next_step_handler(quest_msg, get_inf_about_dctr)


def get_inf_about_dctr(message):
    if message.text == '/choose_doctor':
        choose_doctor(message)
    else:
        key = types.InlineKeyboardMarkup()
        if len(get_inf(message.text)) < 1:
            bot.send_message(message.chat.id, f'За вашим запитом нічого не знайдено :( \nПовторіть спробу')
            information_about_doctors(message)
        if len(get_inf(message.text)) > 1:
            data = get_inf(message.text.replace('_', ' '))
            for doctor in data:
                inform = doctor.rsplit(' ')

                conn = sqlite3.connect('regions.sqlite3')
                c = conn.cursor()
                c.execute(f'INSERT INTO doctors (doctor) SELECT "{inform[0]} {inform[1]}" WHERE NOT EXISTS(SELECT 1 FROM doctors WHERE doctor = "{inform[0]} {inform[1]}");')
                conn.commit()

                itembtn = types.InlineKeyboardButton(text=f"{inform[0]} {inform[1]}", callback_data=f"{inform[0]}_{inform[1]}")
                key.add(itembtn)
            bot.send_message(message.chat.id, f'Лікарі за запитом: "{message.text}"', reply_markup=key)

        else:
            bot.reply_to(message, get_inf(message.text))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    conn = sqlite3.connect('regions.sqlite3')
    c = conn.cursor()

    c.execute('SELECT * FROM ident_city')
    cities = []
    for city in list(c):
        cities.append(str(city[1]))

    c.execute('SELECT * FROM doctors')
    doctors = []
    for doctor in list(c):
        doctors.append(doctor[0].replace(' ', '_'))

    c.execute('SELECT * FROM specialty')
    specialtys = []
    for specialty in list(c):
        specialtys.append(specialty[1].replace(' ', '_'))

    columns = 'user_id INTEGER, ' \
              'city TEXT, ' \
              'speciality TEXT' \
              'doctor TEXT'
    c.execute(f'CREATE TABLE IF NOT EXISTS session ({columns})')
    user_id = call.from_user.id
    c.execute(f'INSERT INTO session (user_id) SELECT "{user_id}" WHERE NOT EXISTS(SELECT 1 FROM session WHERE user_id = "{user_id}");')
    conn.commit()

    if call.data == 'w_fn_ls':
        information_about_doctors(call.message)
    elif call.data == 'w_s':
        search_with_alph(call.message)
    elif call.data in cities:

        c.execute(f'UPDATE session SET city = "{call.data}" WHERE user_id = {user_id};')
        conn.commit()
        conn.close()

        enter_first_symbol(call.message)
    elif call.data in specialtys:

        c.execute(f'UPDATE session SET speciality = "{call.data}" WHERE user_id = {user_id};')
        conn.commit()
        conn.close()

        doctors_in_area(call.message)
    elif call.data in doctors:
        bot.reply_to(call.message, get_inf(str(call.data).replace('_', ' ')))


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True, interval=0)
