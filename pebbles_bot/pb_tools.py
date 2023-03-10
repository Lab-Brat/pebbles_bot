from subprocess import PIPE, STDOUT, Popen
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import (
    AuthenticationException,
    NoValidConnectionsError,
)


def security_check(method):
    """
    Attempt to find user ID in uid whitelist,
    allow uid to run command if found,
    block if not found.
    """

    def wrapper(self, message):
        uid = str(message.from_user.id)
        if uid in self.uid_whitelist:
            method(self, message)
            self.log(message, f">@< {uid} was ALLOWED")
        else:
            block_message = (
                "User is not authorized 🚷\n"
                "This incident was reported to FBI‼️"
            )
            self.bot.reply_to(message, block_message)
            self.log(message, f">!< {uid} was BLOCKED")

    return wrapper


class SSH_Tools:
    def __init__(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def ssh_connect(self, host, port, uname, pwd):
        """
        Establish a SSH connection
        """
        try:
            self.client.connect(host, port=port, username=uname, password=pwd)
            return True
        except AuthenticationException:
            return "pass"
        except NoValidConnectionsError:
            return "port"
        except TimeoutError:
            return "time"

    def ssh_disconnect(self):
        """
        Terminate a SSH connection
        """
        self.client.close()

    def ssh_cmd(self, cmd):
        """
        Run a linux command supplied by user,
        output standard output and standard error
        """
        _, stdout, stderr = self.client.exec_command(cmd)
        sout = self.translate_output(stdout)
        serr = self.translate_output(stderr)
        return sout, serr

    def translate_output(self, output, kind="all"):
        """
        Make output human-readible
        """
        stdout_raw = [line.strip("\n") for line in output]
        stdout_fin = ""
        if kind == "all":
            for part in stdout_raw:
                stdout_fin += part + "\n"
        elif kind == "last":
            for part in stdout_raw:
                stdout_fin = part
        return stdout_fin


class Tools:
    def __init__(self):
        pass

    def os_cmd(self, cmd):
        proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        stdout, stderr = proc.communicate()
        errcode = proc.returncode
        return (self.decode(stdout), self.decode(stderr), errcode)

    def decode(self, output):
        if output is not None:
            return output.decode("utf-8")
        else:
            return ""
