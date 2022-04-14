import os
import paramiko
import keyring 
from getpass import getpass
import pyodbc
import urllib 
from sqlalchemy import create_engine
import pandas as pd

def set_credentials(service,username):
    """Save password in keyring. 

    Args:
        service (string): What application the username and password apply to
        username (string): Username for password being saved
    """
    print(f'Write password for {username}:')
    password = getpass()
    keyring.set_password(service,username,password)
    
def set_up_ssh_client():
    """Sett up ssh connection to srd290_lab1. 

    Returns:
        paramiko.SSHClient, paramiko.SSHClient.SFTP. : Connections to remote computer
    """
    #Get credential
    service = 'RockPaperScissors'
    username = 'srd290_lab1'
    server = '10.8.128.233'
    port = 22
    password = keyring.get_password(service,username)
    if password==None: #if password not already saved
        set_credentials(service,username)
        password = keyring.get_password(service,username)
        
    #Set up sshclient
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Establish connection
    ssh.connect(server,port, username,password)
    sftp = ssh.open_sftp()

    return ssh, sftp

def transfer_local_file(local_file, remote_file):
    """Transfer a local file e.g. a movie to srd290_lab1. 

    Args:
        local_file (string): file path to local file
        remote_file (string): file path to remote file on srd290_lab1
    """
    ssh,sftp =set_up_ssh_client()
    sftp.put(local_file,remote_file)
    sftp.close()
    ssh.close()

def connect_to_database():
    """Establish connections with the SQL server on srd290_lab1. 

    Returns:
        pyodbc.connect, sqlalchemy.create_engin: Two connections to the SQL database
    """
    #Set 
    service = 'RockPaperSciccors'    
    server_name = '10.8.128.233'
    database_name = 'RockPaperScissors'
    username = 'SA'
    
    #Get credential
    password = keyring.get_password(service,username)
    if password==None: #if password not already saved
        set_credentials(service,username)
        password = keyring.get_password(service,username)

    print('Driver={ODBC Driver 17 for SQL Server};'
                        f'Server={server_name};'
                        f'Database={database_name};'
                        f'UID={username};'
                        f'PWD={password};'
                        )
    #Set up pyodbc connection
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        f'Server={server_name};'
                        f'Database={database_name};'
                        f'UID={username};'
                        f'PWD={password};'
                        )
                        
    #Set up sqlalchemy engine
    dialect = 'mssql'
    driver='pyodbc'
    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    f"SERVER={server_name};"
                                    f"DATABASE={database_name};"
                                    f"UID={username};"
                                    f"PWD={password}")
    
    sqlalchemy_database_url = "mssql+pyodbc:///?odbc_connect={}".format(params)
    sqlalchemy_engine = create_engine(sqlalchemy_database_url)
    return connection, sqlalchemy_engine

def add_new_movie(dataframe):
    """Add matedata of a movie to the database. For example dataframe see source code.

    Args:
        dataframe (pandas.DataFrame): Containing matadat for movie.
    """
    dataframe.to_sql('movie_data',engine, if_exists='append',index=False)
    
conn, engine = connect_to_database()
cursor = conn.cursor()




