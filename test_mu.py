import unittest
from mu import ManageUsers


# https://docs.python.org/3/library/unittest.html
class TestManageUsers(unittest.TestCase):
    def setUp(self, ):
        self.mu = None

    def tearDown(self):
        if self.mu is not None:
            self.mu.close()
            self.mu = None

    # def test_simple_cmd_invocation(self):
    #     r = self.s.exec_cmd('cat /etc/passwd')
    #     self.assertIn('root', r)

    def test_password_change_alpine(self):
        self.mu = ManageUsers("127.0.0.1", 2222)
        new_password = 'pwd12345-@12121'
        r = self.mu.change_pwd('root', 'root', new_password)
        print('\npasswd result: ', r)

    def test_password_change_ubuntu(self):
        self.mu = ManageUsers("127.0.0.1", 4444)
        new_password = 'pwd12345-@12121'
        r = self.mu.change_pwd('root', 'root', new_password)
        print('\npasswd result: ', r)

if __name__ == '__main__':
    unittest.main()
