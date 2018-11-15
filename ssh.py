import sys
import re

from pexpect import pxssh


class SshCommandExecutor:
    def __init__(self, host, port, user, password, encoding=None):
        self.__host = host
        self.__user = user
        self.__pwd = password
        self.__port = port
        self.__encoding = encoding
        self.__session = None

    @staticmethod
    def __escape_ansi(line):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', line)

    def __do_logout(self):
        try:
            if self.__session is not None and not self.__session.closed:
                self.__session.close()
        finally:
            self.__session = None

    def __do_login(self):
        assert self.__session is None
        self.__session = pxssh.pxssh(timeout=10, echo=True, logfile=sys.stdout, encoding=self.__encoding, options={ "StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
        try:
            login_result = self.__session.login(self.__host, self.__user, self.__pwd, port=self.__port)
            if login_result:
                try:
                    self.__session.sendline()
                    self.__session.prompt()
                except Exception as e:
                    if not self.__session.closed:
                        self.__do_logout()
                    pass
            else:
                raise Exception('Can\'t establish connection')
        except Exception as e:
            if not self.__session.closed:
                self.__session.close()
                self.__session = None
            pass

    def __s(self, create=False):
        try:
            if not create:
                assert self.__session is not None
            else:
                if self.__session is None:
                    self.__do_login()
            return self.__session
        except:
            pass

    def close(self):
        self.__do_logout()

    def exec_cmd(self, cmd, handler=None):
        s = self.__s(create=True)
        s.sendline(cmd)
        s.prompt()
        #output = con.before.splitlines()
        # con.sendline("echo $?")
        # con.prompt(timeout)
        # exitcode = int(''.join(con.before.splitlines()[1:]))
        # if exitcode != 0:
        #     raise CommandFailed(command, output, exitcode)
        if handler is None:
            # print('\n\nHandler is not provided')
            return SshCommandExecutor.__escape_ansi(s.before)
        else:
            # print('\n\nHandler is provided')
            return handler(s)
