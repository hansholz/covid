import telebot
from telebot import types
import sqlite3
from response import get_inf
from response import search_of_city


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


@bot.message_handler(content_types=['text'])
def search_with_alph(message):
    quest_msg = bot.send_message(message.chat.id, f'Введіть назву міста, в якому ви хочете знайти лікаря:')
    bot.register_next_step_handler(quest_msg, identify_city)


def identify_city(message):
    key = types.InlineKeyboardMarkup()
    data = search_of_city(message.text)
    for city in data:
        itembtn = types.InlineKeyboardButton(text=f"{city}", callback_data=f"{city.replace(' ', '_')}")
        key.add(itembtn)
    bot.send_message(message.chat.id, f'Міста за запитом: "{message.text}" \nОберіть необхідне ', reply_markup=key)


def get_inf_specialty(message):
    key = types.InlineKeyboardMarkup()

    conn = sqlite3.connect('regions.sqlite3')
    c = conn.cursor()
    c.execute('SELECT * FROM specialty')

    data = list(c)
    first = str(message.text).strip().lower()
    alph = ('а б в г д е є ж з и і ї й к л м н о п р с т у х ч щ ю я').split(' ')
    if first in alph:
        for spclty in data:
            if str(spclty[1])[0].lower() == first:
                itembtn = types.InlineKeyboardButton(text=f"{spclty[1]}", callback_data=f"{spclty[0]}")
                key.add(itembtn)
        bot.send_message(message.chat.id, f'Спеціальності на букву: {first}', reply_markup=key)


@bot.message_handler(content_types=['text'])
def information_about_doctors(message):
    quest_msg = bot.send_message(message.chat.id, f'Введіть прізвище лікаря:')
    bot.register_next_step_handler(quest_msg, get_inf_about_dctr)


def get_inf_about_dctr(message):
    key = types.InlineKeyboardMarkup()
    if len(get_inf(message.text)) > 1:
        data = get_inf(message.text)
        for doctor in data:
            inform = doctor.rsplit(' ')
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
        cities.append(city[0].replace(' ', '_'))

    if call.data == 'w_fn_ls':
        information_about_doctors(call.message)
    elif call.data == 'w_s':
        search_with_alph(call.message)
    elif call.data in cities:
        get_inf_specialty(call.message)
    else:
        bot.reply_to(call.message, get_inf(str(call.data).replace('_', ' ')))


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
