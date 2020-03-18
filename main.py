import telebot
from telebot import types
import sqlite3
from response import kyiv_doctors

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
def areas(message, region):
    key = types.InlineKeyboardMarkup()

    conn = sqlite3.connect('regions.sqlite3')
    c = conn.cursor()
    c.execute(f'SELECT region FROM regions WHERE id = {region};')
    reg_centrum = list(c)[0][0]
    c.execute(f'SELECT {reg_centrum.replace(" ", "_")} FROM areas')

    data = list(c)
    for name in data:
        if name[0] is not None:
            itembtn = types.InlineKeyboardButton(text=f"{name[0]}", callback_data=f"{name[0].replace(' ', '_')}")
            key.add(itembtn)
    bot.send_message(message.chat.id, f'Choose your area:', reply_markup=key)


@bot.message_handler(content_types=['text'])
def doctors_in_area(message):
    key = types.InlineKeyboardMarkup()
    for name in kyiv_doctors():
        itembtn = types.InlineKeyboardButton(text=f"{name}", callback_data=f"{name}")
        key.add(itembtn)
    bot.send_message(message.chat.id, f'In Kyiv region works:', reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # checking which button have been pressed
    areas(call.message, f'{call.data}')


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
