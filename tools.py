import paramiko

class Tools():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def ssh_connect(self, host, port, uname, pwd):
        self.client.connect(host, port=port, username=uname, password=pwd)
        try:
            self.client.connect(host, port=port, username=uname, password=pwd)
            return True
        except paramiko.ssh_exception.AuthenticationException:
            return 'pass'
        except paramiko.ssh_exception.NoValidConnectionsError:
            return 'port'
        except TimeoutError:
            return 'time'

    def ssh_disconnect(self):
        self.client.close()

    def ssh_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        sout = self.translate_output(stdout)
        serr = self.translate_output(stderr)
        return sout, serr

    def translate_output(self, output):
        stdout_raw = [line.strip('\n') for line in output]
        stdout_fin = ''
        for part in stdout_raw:
            stdout_fin += part + '\n'
        return stdout_fin


if __name__ == '__main__':
    pass
