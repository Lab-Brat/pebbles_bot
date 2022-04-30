import subprocess
import telebot
from telebot import types

with open('/home/labbrat/bot_api.txt', 'r') as f:
    bot_api = f.read()
bot = telebot.TeleBot(bot_api.strip('\n'))

name = ''
surname = ''
age = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/uptime':
        bot.send_message(message.from_user.id, 'enter IP address <IP:port>')
        bot.register_next_step_handler(message, get_ip)
    else:
        bot.send_message(message.from_user.id, 'type /uptime')

def get_ip(message):
    global ip
    ip = message.text
    bot.send_message(message.from_user.id, 'enter password')
    bot.register_next_step_handler(message, get_pass)

def get_pass(message):
    global paswd
    paswd = message.text
    bot.send_message(message.from_user.id, 'enter username')
    bot.register_next_step_handler(message, get_uname)

def get_uname(message):
    global uname
    uname = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='no', callback_data='no')
    keyboard.add(key_no)
    question = f"logging in machine {ip} with user {uname}, correct?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        ansible_cmd = ['ansible', 'all', '-i', ip, '--extra-vars',
                      f'ansible_user={uname} ansible_password={paswd}', '-a' 'uptime']
        ram = subprocess.check_output(ansible_cmd).decode('ascii')
        bot.send_message(call.message.chat.id, ram)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'call /ram again please')


bot.polling(none_stop=True, interval=0)
