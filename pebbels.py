import logging
from socket import gethostbyname
from pb_tools import Tools

from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup as ik_markup,
    InlineKeyboardButton as ik_button
)


class Pebbles:
    def __init__(self, api_key):
        self.bot = TeleBot(api_key)
        self.tt  = Tools()

        logging.basicConfig(
                    format='%(asctime)s %(message)s', 
                    level=logging.INFO,
                    handlers=[
                        logging.FileHandler("pebbles.log"),
                        logging.StreamHandler()
                    ])
        self.logger = logging.getLogger()


        @self.bot.message_handler(commands=['start'])
        def _start(message):
            self.start(message)

        @self.bot.message_handler(commands=['help'])
        def _help(message):
            self.help(message)

        @self.bot.message_handler(commands=['logout'])
        def _logout(message):
            self.logout(message)

        @self.bot.message_handler(commands=['login'])
        def _login(message):
            self.login(message)

        @self.bot.message_handler(commands=['run'])
        def _run(message):
            self.run(message)

        @self.bot.message_handler(content_types=['text'])
        def _rest(message):
            self.rest(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def _callback_worker(call):
            self.callback_worker(call)

        self.bot.polling(interval=0)


    def start(self, message):
        '''
        /start command
        Function: display hello message and show /help link
        '''
        start_message = ("Pebbles, at your service! "
                        "Please type /help for help")
        self.bot.reply_to(message, start_message)
        self.logger.info(f'[{message.from_user.id} called /start command]')

    def help(self, message):
        '''
        /help command
        Funcion: list all available commands
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
        self.logger.info(f'[{message.from_user.id} called /help command]')

    def logout(self, message):
        '''
        /logout command
        Function: terminates paramiko SSH session
        '''
        self.tt.ssh_disconnect()
        self.bot.reply_to(message, 'SSH connection terminated')
        self.logger.info(f'[{message.from_user.id} called /logout command]')

    def login(self, message):
        '''
        /login command
        Function: initialize SSH connection
        '''
        self.logger.info(f'[{message.from_user.id} called /login command]')
        self.bot.send_message(
                    message.from_user.id, 
                    'Enter **IP address**  [format -> IP:port]', 
                    parse_mode='markdown')
        self.bot.register_next_step_handler(message, self.get_ip)
            
    def _valid_ip_hn(self, ip):
        '''
        Check if input is a valid IP address, 
        or try to resolve it in case of a hostname.
        Return a boolean.
        '''
        try:
            gethostbyname(ip)
            return True
        except:
            return False

    def _parse_ip(self, message):
        '''
        Takes <ip>:<port> as input, 
        validates IP and reads it and port into a dict.
        If port is missing, default SSH port is assigned.
        '''
        msg_split = message.text.split(':')
        host = msg_split[0]
        port = '22' if len(msg_split) == 1 else msg_split[1]
        resolved = True if self._valid_ip_hn(msg_split[0]) else False
        return {'host': host, 
                'port': port,
                'resolved': resolved}

    def get_ip(self, message):
        '''
        Takes IP address and port of the remote host as input,
        redirects to get_uname
        '''
        self.logger.info(f'[{message.from_user.id} called get_ip method]')
        self.host = self._parse_ip(message)
        if not self.host['resolved']:
            err_message = f"{self.host['host']} cannot be resolved"
            self.bot.send_message(message.from_user.id, err_message)
            self.logger.info(f"[{message.from_user.id} {err_message}")
        else:
            self.bot.send_message(
                        message.from_user.id,
                        'Enter **username**',
                        parse_mode='markdown')
            self.bot.register_next_step_handler(message, self.get_uname)

    def get_uname(self, message):
        '''
        Takes username of the remote host as input,
        redirects to get_pass
        '''
        self.logger.info(f'[{message.from_user.id} called get_uname method]')
        self.uname = message.text
        self.bot.send_message(
                    message.from_user.id,
                    'Enter **password**',
                    parse_mode='markdown')
        self.bot.register_next_step_handler(message, self.get_pass)

    def get_pass(self, message):
        '''
        Takes remote host's password as input,
        displays confirmation message
        '''
        self.logger.info(f'[{message.from_user.id} called get_pass method]')
        self.paswd = message.text

        keyboard = ik_markup()
        keyboard.add(ik_button(text='yes', callback_data='yes'))
        keyboard.add(ik_button(text='no', callback_data='no'))
        question = (f"Establish SSH connection to " 
                    f"{self.host['host']}:{self.host['port']} "
                    f"with user `{self.uname}`?")

        self.bot.send_message(
                    message.from_user.id,
                    text=question, 
                    reply_markup=keyboard, 
                    parse_mode="markdown")
        
    def run(self, message):
        '''
        /run command
        Function: run a Linux command
        '''
        self.bot.reply_to(message, "Enter command to run: ")
        self.bot.register_next_step_handler(message, self.run_command)

    def run_command(self, message):
        '''
        Receives command from /run
        runs it using methods from pb_tools.py
        '''
        try:
            cout, err = self.tt.ssh_cmd(message.text)
            if cout != '' and err != '':
                self.bot.send_message(
                    message.from_user.id,
                    f'Command output: \n{cout}\n')
                self.bot.send_message(
                    message.from_user.id,
                    f'Command output: \n{err}')
            elif cout != '':
                self.bot.send_message(message.from_user.id, cout)
            elif err != '':
                self.bot.send_message(message.from_user.id, err)
            elif cout == '' and err == '':
                self.bot.send_message(
                    message.from_user.id,
                    'No Output')
        except AttributeError:
            err_msg = 'There is no active SSH session'
            self.bot.send_message(message.from_user.id, err_msg)
        self.logger.info(f'[{message.from_user.id} called /run command]')

    def callback_worker(self, call):
        '''
        Process callback data from the confirmation message,
        if callback is yes - establish a SSH connection,
        if callback is no - suggest to run /login again
        '''
        if call.data == "yes":
            con_result = self.tt.ssh_connect(
                                self.host['host'], 
                                self.host['port'], 
                                self.uname, 
                                self.paswd)
            if con_result == True:
                self.bot.send_message(
                    call.message.chat.id,
                    'Login Success')
            elif con_result == 'pass':
                self.bot.send_message(
                    call.message.chat.id,
                    'Login Failed, Wrong Password')
            elif con_result == 'port':
                self.bot.send_message(
                    call.message.chat.id,
                    'Login Failed, Wrong Port')
            elif con_result == 'time':
                self.bot.send_message(
                    call.message.chat.id,
                    'Login Failed, Connection Timed Out')
            self.logger.info(f'[user pressed YES on the keyboard]')
        elif call.data == "no":
            self.bot.send_message(
                call.message.chat.id,
                'To start over enter /login again')
            self.logger.info(f'[user pressed NO on the keyboard]')

    def rest(self, message):
        '''
        Process input that is not defined
        '''
        self.bot.send_message(message.from_user.id,
                'I do not understand :( \ncall /help for help')
