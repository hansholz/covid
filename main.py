import telebot
from telebot import types
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
    with open("regions.txt") as reg:
        id = 0
        for region in reg:
            id += 1
            itembtn = types.InlineKeyboardButton(text=f"{region}", callback_data=f"{id}")
            key.add(itembtn)
    bot.send_message(message.chat.id, f'Which region you need?', reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # checking which button have been pressed
    if call.data == "1":
        bot.send_message(call.message.chat.id, f'Vinnytsya')
    elif call.data == "9":
        bot.send_message(call.message.chat.id, f'{kyiv_doctors()}')


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
