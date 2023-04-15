import os
from subprocess import PIPE, STDOUT, Popen
from paramiko import SSHConfig, SSHClient, AutoAddPolicy
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
        self.config = SSHConfig()
        self.read_ssh_config()

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def read_ssh_config(self):
        """
        Read SSH config file and return a dictionary
        """
        ssh_config_file = os.path.expanduser("~/.ssh/config")
        with open(ssh_config_file) as f:
            self.config.parse(f)

    def ssh_connect(self, host):
        """
        Establish a SSH connection
        """
        try:
            host_config = self.config.lookup(host)
            if "identityfile" not in host_config:
                return "key_not_found"
            else:
                self.client.connect(
                    host_config["hostname"],
                    username=host_config.get("user"),
                    port=host_config.get("port"),
                    key_filename=host_config.get("identityfile"),
                )
                return True
        except TimeoutError:
            return "timeout"
        except:
            return "config_not_found"

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
