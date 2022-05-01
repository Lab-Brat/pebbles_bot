import subprocess
import telebot
from telebot import types
from datetime import datetime as dt

linux_user = subprocess.getoutput("echo $USER")

with open(f"/home/{linux_user}/bot_api.txt", 'r') as f:
    bot_api = f.read()
bot = telebot.TeleBot(bot_api.strip('\n'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Pebbles, at your service! Please type /help for help")
    print(f'[{message.from_user.id} called /start method at {dt.now()}]')

@bot.message_handler(commands=['help'])
def help(message):
    l0 = "Commands that Pebbles know:\n"
    c1 = "/start -----------> display start message\n"
    c2 = "/help ------------> display help message\n"
    c3 = "/send_cmd ---> send a command to a Linux host"
    help_message = f"{l0}{c1}{c2}{c3}"
    bot.reply_to(message, help_message)
    print(f'[{message.from_user.id} called /help method at {dt.now()}]')

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/send_cmd':
        bot.send_message(message.from_user.id, 'enter IP address <IP>:<port>')
        bot.register_next_step_handler(message, get_ip)
        print(f'[{message.from_user.id} called get_ip method at {dt.now()}]')
    else:
        bot.send_message(message.from_user.id, 'I only know /send_cmd for now')

def get_ip(message):
    global ip
    ip = message.text
    bot.send_message(message.from_user.id, 'enter password')
    bot.register_next_step_handler(message, get_pass)
    print(f'[{message.from_user.id} called get_pass method at {dt.now()}]')

def get_pass(message):
    global paswd
    paswd = message.text
    bot.send_message(message.from_user.id, 'enter username')
    bot.register_next_step_handler(message, get_uname)
    print(f'[{message.from_user.id} called get_uname method at {dt.now()}]')

def get_uname(message):
    global uname
    uname = message.text
    bot.send_message(message.from_user.id, 'enter command')
    bot.register_next_step_handler(message, get_cmd)
    print(f'[{message.from_user.id} called get_cmd method at {dt.now()}]')

def get_cmd(message):
    global cmd
    cmd = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='no', callback_data='no')
    keyboard.add(key_no)
    question1 = f"logging on to that machine {ip} with user `{uname}`, "
    question2 = f"running command `{cmd}`"
    question = question1 + question2
    bot.send_message(message.from_user.id, text=question, 
                     reply_markup=keyboard, parse_mode="markdown")
    print(f'[{message.from_user.id} was promted to verify data at {dt.now()}]')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        ansible_cmd = ['ansible', 'all', '-i', f'{ip},', '--extra-vars',
                      f'ansible_user={uname} ansible_password={paswd}', '-a', cmd]
        ram = subprocess.check_output(ansible_cmd).decode('utf-8')
        bot.send_message(call.message.chat.id, ram)
        print(f'[user pressed YES on the keyboard and got ansible output at {dt.now()}]')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'call /send_cmd again please')
        print(f'[user pressed NO on the keyboard] at {dt.now()}]')


bot.polling(interval=0)
