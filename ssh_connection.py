import os
import cv2
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
        """Set up ssh connection to srd290_lab1.
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
        """Transfer a local file e.g. a movie to remote desktop.

        Args:
            local_file (string): file path to local file
            remote_file (string): file path to remote file on srd290_lab1
        """
        self.sftp.put(local_file, remote_file)

    def delete_remote_file(self,remote_files):
        """Delete file e.g. a movie on the remote desktop.

        Args:
            remote_files (list): A list of file paths to be removed.
        """
        for remote_file in remote_files:
            print(remote_file)
            self.sftp.remove(remote_file)
    
    def watch_remote_movie(self,remote_file):
        """Watch a recorded video located on the remote desktop.

        Args:
            remote_file (string): File path to the video on the remote desktop.
        """
        
        #Transfer remote file to local file
        temporary_local_file = 'temp_file.mp4'
        self.sftp.get(remotepath=remote_file, localpath=temporary_local_file)
        
        #Play movie
        cap = cv2.VideoCapture(temporary_local_file)
        if cap.isOpened()==False:
            print("Error opening video file")
        while cap.isOpened():
            ret,frame=cap.read()
            if ret==True:
                cv2.imshow('Frame',frame)
                if cv2.waitKey(25)==ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        
        #Delete local file
        os.remove(temporary_local_file)