import keyring
from getpass import getpass


class Credentials:
    @staticmethod
    def set_credentials(service, username):
        """Save password in keyring.

        Args:
            service (string): What application the username and password apply to
            username (string): Username for password being saved
        """
        print(f'Write password for {username}:')
        password = getpass()
        keyring.set_password(service, username, password)

    @classmethod
    def get_credentials(cls, service, username):
        password = keyring.get_password(service, username)
        if password is None: #if password not already saved
            cls.set_credentials(service, username)
            password = keyring.get_password(service, username)
        return password



