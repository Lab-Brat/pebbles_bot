import fabric
import paramiko

class Tools():
    def __init__(self):
        # instantiate paramiko ssh client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def ssh_connect(self, host, port, uname, pwd):
        '''
        Establish ssh connection
        '''
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
        '''
        Terminate ssh connection
        '''
        self.client.close()

    def ssh_cmd(self, cmd):
        '''
        Run a linux command supplied by the user,
        output standard output and standard error
        '''
        stdin, stdout, stderr = self.client.exec_command(cmd)
        sout = self.translate_output(stdout)
        serr = self.translate_output(stderr)
        return sout, serr

    def translate_output(self, output, kind='all'):
        '''
        Make output human-readible
        '''
        stdout_raw = [line.strip('\n') for line in output]
        stdout_fin = ''
        if kind == 'all':
            for part in stdout_raw:
                stdout_fin += part + '\n'
        elif kind == 'last':
            for part in stdout_raw:
                stdout_fin = part
        return stdout_fin


if __name__ == '__main__':
    pass
