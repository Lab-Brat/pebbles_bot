import telebot
from telebot import types
from datetime import datetime as dt
from pb_tools import Tools

try:
    with open(f"pebbles_api", 'r') as api_key:
        bot_api = api_key.read()
    print("Pebbles has started!")
except FileNotFoundError:
    print("pebbles_api key file is not in the repo")
    raise SystemExit(0)

class Pebbles:
    def __init__(self):
        self.bot = telebot.TeleBot(bot_api.strip('\n'))

        @self.bot.message_handler(commands=['start'])
        def _start(message):
            self.start(message)

        @self.bot.message_handler(commands=['help'])
        def _help(message):
            self.help(message)

        self.bot.polling(interval=0)


    def start(self, message):
        '''
        Bot's /start command, 
        display hello message and show /help link
        '''
        start_message = ("Pebbles, at your service! "
                        "Please type /help for help")
        self.bot.reply_to(message, start_message)
        print(f'[{message.from_user.id} called /start method at {dt.now()}]')

    def help(self, message):
        '''
        Bot's /help command, list all available commands
        '''
        help_message = (
            "Commands that Pebbles knows:\n"
            "/start -------> display start message\n"
            "/help --------> display help message\n"
            "/login -------> send a command to a Linux host\n"
            "/logout -----> terminate ssh session\n"
            "/run ---------> run a linux command"
        )
        self.bot.reply_to(message, help_message)
        print(f'[{message.from_user.id} called /help method at {dt.now()}]')

    # @self.bot.message_handler(commands=['logout'])
    # def logout(message):
    #     '''
    #     Bot's /logout command, 
    #     terminates paramiko SSH session
    #     '''
    #     Tools().ssh_disconnect()
    #     bot.send_message(message.from_user.id, 'Session Terminated')

    # @self.bot.message_handler(content_types=['text'])
    # def start(self, message):
    #     '''
    #     Main sequence that processes all strings and commands with redirects
    #     '''
    #     if message.text == '/login': # establish a SSH connection to host
    #         bot.send_message(message.from_user.id, 
    #                         'Enter **IP address**  [format -> IP:port]', 
    #                         parse_mode='markdown')
    #         bot.register_next_step_handler(message, self.get_ip)
    #         print(f'[{message.from_user.id} called get_ip method at {dt.now()}]')
    #     elif message.text == '/run': # run a linux command
    #         bot.reply_to(message, "Enter command to run: ")
    #         bot.register_next_step_handler(message, self.run)
    #     else:
    #         bot.send_message(message.from_user.id, 
    #                         'I do not understand :( \ncall /help for help')

    # def get_ip(self, message):
    #     '''
    #     Takes IP address and port of the remote host as input,
    #     redirects to get_uname
    #     '''
    #     global ip
    #     ip = message.text.split(':')
    #     bot.send_message(message.from_user.id,
    #                     'Enter **username**',
    #                     parse_mode='markdown')
    #     bot.register_next_step_handler(message, self.get_uname)
    #     print(f'[{message.from_user.id} called get_uname method at {dt.now()}]')

    # def get_uname(self, message):
    #     '''
    #     Takes username of the remote host as input,
    #     redirects to get_pass
    #     '''
    #     global uname
    #     uname = message.text
    #     bot.send_message(message.from_user.id, 'Enter **password**', parse_mode='markdown')
    #     bot.register_next_step_handler(message, self.get_pass)
    #     print(f'[{message.from_user.id} called get_pass method at {dt.now()}]')

    # def get_pass(self, message):
    #     '''
    #     Takes remote host's password as input,
    #     displays confirmation message
    #     '''
    #     global paswd
    #     paswd = message.text

    #     keyboard = types.InlineKeyboardMarkup()
    #     key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
    #     keyboard.add(key_yes)
    #     key_no= types.InlineKeyboardButton(text='no', callback_data='no')
    #     keyboard.add(key_no)
    #     question = f"logging on to that machine {ip[0]}:{ip[1]} with user `{uname}`"

    #     bot.send_message(message.from_user.id, text=question, 
    #                     reply_markup=keyboard, parse_mode="markdown")
    #     print(f'[{message.from_user.id} was promted to verify data at {dt.now()}]')

    # def run(self, message):
    #     '''
    #     Runs a linux error, returns stdout or stderr depending on the output
    #     '''
    #     global cmd
    #     cmd = message.text
    #     try:
    #         cout, err = Tools.ssh_cmd(cmd)
    #         if cout != '' and err != '':
    #             bot.send_message(message.from_user.id, f'Command output: \n{cout}\n')
    #             bot.send_message(message.from_user.id, f'Command output: \n{err}')
    #         elif cout != '':
    #             bot.send_message(message.from_user.id, cout)
    #         elif err != '':
    #             bot.send_message(message.from_user.id, err)
    #         elif cout == '' and err == '':
    #             bot.send_message(message.from_user.id, 'No Output')
    #     except AttributeError:
    #         err_msg = 'There is no active SSH session'
    #         bot.send_message(message.from_user.id, err_msg)
    #     print(f'[{message.from_user.id} called /run method at {dt.now()}]')


    # @self.bot.callback_query_handler(func=lambda call: True)
    # def callback_worker(self, call):
    #     '''
    #     Process callback data from the confirmation message,
    #     if callback is yes - establish a SSH connection,
    #     if callback is no - suggest to run /login again
    #     '''
    #     if call.data == "yes":
    #         con_result = Tools().ssh_connect(ip[0], ip[1], uname, paswd)
    #         if con_result == True:
    #             bot.send_message(call.message.chat.id, 'Login Success')
    #         elif con_result == 'pass':
    #             bot.send_message(call.message.chat.id, 'Login Failed, Wrong Password')
    #         elif con_result == 'port':
    #             bot.send_message(call.message.chat.id, 'Login Failed, Wrong Port')
    #         elif con_result == 'time':
    #             bot.send_message(call.message.chat.id, 'Login Failed, Connection Timed Out')
    #         print(f'[user pressed YES on the keyboard at {dt.now()}]')
    #     elif call.data == "no":
    #         bot.send_message(call.message.chat.id, 'To start over enter /login again')
    #         print(f'[user pressed NO on the keyboard] at {dt.now()}]')


if __name__ == '__main__':
    pebbles = Pebbles()
