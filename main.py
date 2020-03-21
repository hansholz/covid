import telebot
from telebot import types
import sqlite3
from response import get_inf


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
    itembtn = types.InlineKeyboardButton(text=f"With firstname and lastname", callback_data=f"w_fn_ls")
    key.add(itembtn)
    bot.send_message(message.chat.id, f'How i can help you to find doctor?', reply_markup=key)


@bot.message_handler(commands=['regions'])
def search_a_doctor(message):
    key = types.InlineKeyboardMarkup()

    conn = sqlite3.connect('regions.sqlite3')
    c = conn.cursor()
    c.execute('SELECT * FROM regions')

    data = list(c)
    for region in data:
        itembtn = types.InlineKeyboardButton(text=f"{region[1]}", callback_data=f"{region[0]}")
        key.add(itembtn)
    bot.send_message(message.chat.id, f'Which region you need? ', reply_markup=key)
    conn.close()


@bot.message_handler(content_types=['text'])
def information_from_input_fn_ln(message):
    key = types.InlineKeyboardMarkup()
    if len(get_inf(message.text)) > 1:
        data = get_inf(message.text)
        for doctor in data:
            inform = doctor.rsplit(' ')
            itembtn = types.InlineKeyboardButton(text=f"{inform[0]} {inform[1]}", callback_data=f"{inform[0]}_{inform[1]}")
            key.add(itembtn)
        bot.send_message(message.chat.id, f'Doctors with name "{message.text}"', reply_markup=key)

    else:
        bot.reply_to(message, get_inf(message.text))


@bot.message_handler(content_types=['text'])
def information_from_input_fn_ln(message):
    bot.send_message(message.chat.id, f'Enter first name and last name:')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'w_fn_ls':
        information_from_input_fn_ln(call.message)
    else:
        bot.reply_to(call.message, get_inf(str(call.data).replace('_', ' ')))



bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
