import logging
from pathlib import Path
from .pb_tools import security_check, Tools, SSH_Tools

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (
    InlineKeyboardMarkup as ik_markup,
    InlineKeyboardButton as ik_button,
)


class Pebbles:
    def __init__(self, api_key, whitelist, notify=False):
        self.bot = TeleBot(api_key)
        self.tls = Tools()
        self.ssh = SSH_Tools()
        self.pebbles_mode = "local"

        self.uid_whitelist = whitelist

        logging.basicConfig(
            format="%(asctime)s %(message)s",
            level=logging.INFO,
            handlers=[
                logging.FileHandler(f"{str(Path.home())}/.pebbles.log"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger()

        @self.bot.message_handler(commands=["start"])
        def _start(message):
            self.start(message)

        @self.bot.message_handler(commands=["help"])
        def _help(message):
            self.help(message)

        @self.bot.message_handler(commands=["logout"])
        def _logout(message):
            self.logout(message)

        @self.bot.message_handler(commands=["login"])
        def _login(message):
            self.login(message)

        @self.bot.message_handler(commands=["run"])
        def _run(message):
            self.run(message)

        @self.bot.message_handler(commands=["mode"])
        def _mode(message):
            self.mode(message)

        @self.bot.message_handler(content_types=["text"])
        def _rest(message):
            self.rest(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def _callback_worker(call):
            self.callback_worker(call)

        if notify:
            self.send_notification(notify)
        else:
            self.start_bot()

    def start_bot(self):
        """
        Start the bot and print a message.
        """
        self.logger.info("Pebbles is awakening...")
        self.logger.info("Awaiting commands")
        try:
            self.bot.polling(interval=0)
        except ApiTelegramException:
            self.logger.info("Unable to start Pebbles, check your API key")
        self.logger.info("Pebbles is entering hibernation...")

    def log(self, info, log=""):
        """
        Simplifies the use of logger library,
        and makes logger look cleaner in the code.
        """
        uid = info.from_user.id
        if "/" in log:
            self.logger.info(f"[{uid} called {log} command]")
        else:
            self.logger.info(f"[{uid} {log}]")

    def send_notification(self, text):
        """
        Send a notification to the user.
        """
        for user_id in self.uid_whitelist:
            intro = "📢 Notification from Pebbles 📢"
            self.bot.send_message(user_id, intro)
            self.bot.send_message(user_id, text)

    @security_check
    def start(self, message):
        """
        /start command
        Function: display hello message and show /help link
        """
        self.log(message, log="/start")
        start_message = (
            "Pebbles, at your service! 🐧\n" "Please type /help for help"
        )
        self.bot.reply_to(message, start_message)

    @security_check
    def help(self, message):
        """
        /help command
        Funcion: list all available commands
        """
        self.log(message, log="/help")
        help_message = (
            "Commands that Pebbles knows 🎁:\n"
            "/start -------> display start message\n"
            "/help --------> display help message\n"
            "/mode --------> change mode between local and remote\n"
            "/login -------> send a command to a Linux host\n"
            "/logout -----> terminate ssh session\n"
            "/run ---------> run a linux command"
        )
        self.bot.reply_to(message, help_message)

    @security_check
    def logout(self, message):
        """
        /logout command
        Function: terminates paramiko SSH session
        """
        self.log(message, log="/logout")
        self.ssh.ssh_disconnect()
        self.bot.reply_to(message, "SSH connection terminated ⚡️")

    @security_check
    def login(self, message):
        """
        /login command
        Function: initialize SSH connection
        """
        self.log(message, log="/login")
        self.bot.send_message(
            message.from_user.id,
            "Enter *hostname*\n(as defined in `~/.ssh/config`)",
            parse_mode="markdown",
        )
        self.bot.register_next_step_handler(message, self.get_hostname)

    def get_hostname(self, message):
        """
        Takes hostname (as defined in ~/.ssh/config),
        """
        self.log(message, "called get_hostname method")
        self.host = message.text
        keyboard = ik_markup()
        keyboard.add(ik_button(text="yes", callback_data="yes"))
        keyboard.add(ik_button(text="no", callback_data="no"))
        question = f"Establish SSH connection to {self.host}"

        self.bot.send_message(
            message.from_user.id,
            text=question,
            reply_markup=keyboard,
            parse_mode="markdown",
        )

    @security_check
    def run(self, message):
        """
        /run command
        Function: runs a shell command locally or on a remote
                  server, depending on mode
        """
        self.log(message, log="/run")
        self.bot.reply_to(message, "Enter command to run: ")
        self.bot.register_next_step_handler(message, self.run_command)

    @security_check
    def mode(self, message):
        """
        /mode command
        Function: Switch mode between local and remote
        """
        self.log(message, log="/mode")
        keyboard = ik_markup()
        keyboard.add(ik_button(text="Locally", callback_data="local"))
        keyboard.add(ik_button(text="Remotely", callback_data="remote"))
        question = f"Run commands ..."

        self.bot.send_message(
            message.from_user.id,
            text=question,
            reply_markup=keyboard,
            parse_mode="markdown",
        )

    def run_command(self, message):
        """
        Receives command from /run_command
        runs it using methods from pb_tools.py
        """
        try:
            if self.pebbles_mode == "remote":
                cout, err = self.ssh.ssh_cmd(message.text)
                self.log(message, f"ran (remote) => {message.text}")
            elif self.pebbles_mode == "local":
                cout, err, _ = self.tls.os_cmd(message.text)
                self.log(message, f"ran => {message.text}")
            if cout != "" and err != "":
                self.bot.send_message(
                    message.from_user.id, f"Command output: \n{cout}\n"
                )
                self.bot.send_message(
                    message.from_user.id, f"Error output: \n{err}"
                )
            elif cout != "":
                self.bot.send_message(message.from_user.id, cout)
            elif err != "":
                self.bot.send_message(message.from_user.id, err)
            elif cout == "" and err == "":
                self.bot.send_message(message.from_user.id, "No Output")
        except AttributeError:
            err_msg = "There is no active SSH session"
            self.bot.send_message(message.from_user.id, err_msg)

    def _connect(self, chat_id, con_result):
        """
        Use Paramiko to connect to remote host,
        return connection status.
        """
        if con_result == True:
            self.bot.send_message(chat_id, "Login Success 🔗")
        elif con_result == "key_not_found":
            self.bot.send_message(chat_id, "Login Failed, No Key In Config ❌")
        elif con_result == "timeout":
            self.bot.send_message(
                chat_id, "Login Failed, Connection Timed Out ❌"
            )
        elif con_result == "config_not_found":
            self.bot.send_message(
                chat_id, "Login Failed, ~/.ssh/config File Not Found ❌"
            )
        else:
            self.bot.send_message(chat_id, "Login Failed, Reason Unclear ❌")

    def callback_worker(self, call):
        """
        Process callback data from the confirmation message,
        if callback is yes - establish a SSH connection,
        if callback is no - suggest to run /login again
        """
        if call.data == "yes":
            self.log(call, "pressed YES on the keyboard")
            con_result = self.ssh.ssh_connect(self.host)
            self._connect(call.message.chat.id, con_result)
        elif call.data == "no":
            self.log(call, "pressed NO on the keyboard")
            self.bot.send_message(
                call.message.chat.id, "To start over enter /login again ♻️"
            )
        elif call.data == "remote":
            self.pebbles_mode = "remote"
            self.bot.send_message(
                call.message.chat.id, "Pebbles mode: Remote 🚀"
            )
        elif call.data == "local":
            self.pebbles_mode = "local"
            self.bot.send_message(
                call.message.chat.id, "Pebbles mode: Local 🏡"
            )

    def rest(self, message):
        """
        Process input that is not defined
        """
        self.bot.send_message(
            message.from_user.id,
            "I do not understand :( \ncall /help for help",
        )
