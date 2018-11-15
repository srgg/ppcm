from ssh import SshCommandExecutor


class ManageUsers:
    def __init__(self, host, port=22, encoding='utf-8'):
        self.__ssh = None
        self.__host = host
        self.__port = port
        self.__encoding = encoding

    def close(self):
        if self.__ssh is not None:
            self.__ssh = None
            self.__ssh.close()

    def change_pwd(self, user, old_pwd, new_pwd):
        ssh = SshCommandExecutor(self.__host, self.__port, user, old_pwd, encoding=self.__encoding)
        try:
            ssh.exec_cmd('passwd', lambda session : self.__handle_change_pw(session, new_pwd))
        finally:
            ssh.close()

    @staticmethod
    def __send_line(session, line):
        session.sendline(line)
        session.expect('\s*\r\n')

    @staticmethod
    def __consume_eol(session):
        session.expect('\s*\r\n')

    def __handle_change_pw(self, s, new_pwd):
        # Ubuntu

        # Happy Path scenario
        # -------------------
        #$passwd
        #Enter new UNIX password:
        #Retype new UNIX password:
        #passwd: password updated successfully

        # Alpine

        # Happy Path scenario
        # -------------------
        #>passwd
        #Changing password for root
        #New password:
        #Retype password:
        #passwd: password for root changed by root

        # Short password Failure scenario
        # -------------------
        #passwd
        #Changing password for root
        #New password:
        #Bad password: too short
        #Retype password:

        r0 = s.expect(['Changing password for ([^\r]*)\r\n', '(?=Enter new UNIX password)'])
        if r0 == 0:
            # Alpine
            ulogin = s.match.group(1)
        else:
            # Ubuntu
            ulogin = 'unknown'

        print('\nr0: option ', r0, ' user: <' + ulogin + '>')

        r1 = s.expect(r'.*(?:New password|Enter new UNIX password):')
        print('\nr1: option ', r1 )
        self.__send_line(s, new_pwd)

        r2 = s.expect([r'Bad password:([^\r]+)', r'(?:Retype password|Retype new UNIX password):\s*$'])
        print('\nr2: option ', r2 )

        if r2 == 0:
            # Something wrong with the password
            # print('Bad password, exception will be raised, error: ', s.match.group(1))

            # Bad password
            raise Exception('Can\'set a new password: ' + s.match.group(1))

        # Needs to retype password
        # print('New password accepted, needs to retype')
        self.__send_line(s, new_pwd)

        # Consume resulting message
        r3 = s.expect(['passwd: password for ([^ ]*) changed by ([^\r]*)', 'passwd: password updated successfully'])
        if r3 == 0:
            # Alpine
            changed_for = s.match.group(1)
            changed_by = s.match.group(2)
        else:
            # Ubuntu
            changed_for = 'unknown'
            changed_by = 'unknown'

        print('\nr3: option ', r3, 'changed by: <'+changed_by+'>, changed for: <' + changed_for + '>' )
        self.__consume_eol(s)

        # Match prompt
        s.prompt()
        print('\nprompt matched')
        return s.before
