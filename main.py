import subprocess
import telebot
from telebot import types
from datetime import datetime as dt
from tools import Tools

# get Linux host username
linux_user = subprocess.getoutput("echo $USER")
tt = Tools()

# read bot api hash
try:
    with open(f"/home/{linux_user}/bot_api.txt", 'r') as f:
        bot_api = f.read()
    bot = telebot.TeleBot(bot_api.strip('\n'))
    print("Pebbles has started!")
except FileNotFoundError:
    print("File is not at /home/$USER, or incorrect filename")
    raise SystemExit(0)

@bot.message_handler(commands=['start'])
def start(message):
    '''
    Bot's /start command, display hello message and show /help link
    '''
    bot.reply_to(message, "Pebbles, at your service! Please type /help for help")
    print(f'[{message.from_user.id} called /start method at {dt.now()}]')

# bot's help command
@bot.message_handler(commands=['help'])
def help(message):
    '''
    Bot's /help command, list all available commands
    '''
    l0 = "Commands that Pebbles knows:\n"
    c1 = "/start -------> display start message\n"
    c2 = "/help --------> display help message\n"
    c3 = "/login -------> send a command to a Linux host\n"
    c4 = "/logout -----> terminate ssh session\n"
    c5 = "/run ---------> run a linux command"
    help_message = f"{l0}{c1}{c2}{c3}{c4}{c5}"
    bot.reply_to(message, help_message)
    print(f'[{message.from_user.id} called /help method at {dt.now()}]')

@bot.message_handler(commands=['logout'])
def logout(message):
    '''
    Bot's /logout command, terminates paramiko SSH session
    '''
    tt.ssh_disconnect()
    bot.send_message(message.from_user.id, 'Session Terminated')

@bot.message_handler(content_types=['text'])
def start(message):
    '''
    Main sequence that processes all strings and commands with redirects
    '''
    if message.text == '/login':
        # Bot's /login command, establishes SSH connection with paramiko
        entip = 'Enter **IP address**, format ---> IP:port'
        bot.send_message(message.from_user.id, entip, parse_mode='markdown')
        bot.register_next_step_handler(message, get_ip)
        print(f'[{message.from_user.id} called get_ip method at {dt.now()}]')
    elif message.text == '/run':
        # bot's run command, runs a linux command
        bot.reply_to(message, "Enter command to run: ")
        bot.register_next_step_handler(message, run)
    else:
        # display /help command if users input is not recognized
        bot.send_message(message.from_user.id, 'I do not understand :(, call /help for help')

def get_ip(message):
    '''
    Takes IP address and port of the remote host as input,
    redirects to get_uname
    '''
    global ip
    ip = message.text.split(':')
    bot.send_message(message.from_user.id, 'Enter **username**', parse_mode='markdown')
    bot.register_next_step_handler(message, get_uname)
    print(f'[{message.from_user.id} called get_uname method at {dt.now()}]')

def get_uname(message):
    '''
    Takes username of the remote host as input,
    redirects to get_pass
    '''
    global uname
    uname = message.text
    bot.send_message(message.from_user.id, 'Enter **password**', parse_mode='markdown')
    bot.register_next_step_handler(message, get_pass)
    print(f'[{message.from_user.id} called get_pass method at {dt.now()}]')

def get_pass(message):
    '''
    Takes remote host's password as input,
    displays confirmation message
    '''
    global paswd
    paswd = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='no', callback_data='no')
    keyboard.add(key_no)
    question = f"logging on to that machine {ip[0]}:{ip[1]} with user `{uname}`"

    bot.send_message(message.from_user.id, text=question, 
                     reply_markup=keyboard, parse_mode="markdown")
    print(f'[{message.from_user.id} was promted to verify data at {dt.now()}]')

def run(message):
    '''
    Runs a linux error, returns stdout or stderr depending on the output
    '''
    global cmd
    cmd = message.text
    try:
        cout, err = tt.ssh_cmd(cmd)
        if cout != '' and err != '':
            bot.send_message(message.from_user.id, f'Command output: \n{cout}\n')
            bot.send_message(message.from_user.id, f'Command output: \n{err}')
        elif cout != '':
            bot.send_message(message.from_user.id, cout)
        elif err != '':
            bot.send_message(message.from_user.id, err)
        elif cout == '' and err == '':
            bot.send_message(message.from_user.id, 'No Output')
    except AttributeError:
        err_msg = 'There is no active SSH session'
        bot.send_message(message.from_user.id, err_msg)
    print(f'[{message.from_user.id} called /run method at {dt.now()}]')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    '''
    Process callback data from the confirmation message,
    if callback is yes - establish a SSH connection,
    if callback is no - suggest to run /login again
    '''
    if call.data == "yes":
        con_result = tt.ssh_connect(ip[0], ip[1], uname, paswd)
        if con_result == True:
            bot.send_message(call.message.chat.id, 'Login Success')
        elif con_result == 'pass':
            bot.send_message(call.message.chat.id, 'Login Failed, Wrong Password')
        elif con_result == 'port':
            bot.send_message(call.message.chat.id, 'Login Failed, Wrong Port')
        elif con_result == 'time':
            bot.send_message(call.message.chat.id, 'Login Failed, Connection Timed Out')
        print(f'[user pressed YES on the keyboard at {dt.now()}]')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'To start over enter /login again')
        print(f'[user pressed NO on the keyboard] at {dt.now()}]')

# keep running the bot
bot.polling(interval=0)
