import paramiko
from credentials import Credentials


class SSHConnection:
    def __init__(self, service, username, server, port):
        self.service = service
        self.username = username
        self.server = server
        self.port = port
        self.cred = Credentials()
        self.set_up_ssh_client()

    def close(self):
        self.sftp.close()
        self.ssh.close()


    def set_up_ssh_client(self):
        """Sett up ssh connection to srd290_lab1.

        Returns:
            paramiko.SSHClient, paramiko.SSHClient.SFTP. : Connections to remote computer
        """
        #Get credentials
        password = self.cred.get_credentials(self.service, self.username)

        #Set up sshclient
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Establish connection
        self.ssh.connect(self.server, self.port, self.username, password)
        self.sftp = self.ssh.open_sftp()


    def transfer_local_file(self, local_file, remote_file):
        """Transfer a local file e.g. a movie to srd290_lab1.

        Args:
            local_file (string): file path to local file
            remote_file (string): file path to remote file on srd290_lab1
        """
        self.sftp.put(local_file, remote_file)
