import pyodbc
import urllib
from sqlalchemy import create_engine
from credentials import Credentials


class SQLConnection:
    def __init__(self, service, username, server, database):
        self.service = service
        self.username = username
        self.server = server
        self.database = database
        self.cred = Credentials()
        self.connect_to_database()

    def close(self):
        self.sqlalchemy_engine.dispose()
        self.connection.close()

    def connect_to_database(self):
        """Establish connections with the SQL server on srd290_lab1.
        """
        #Get credentials
        password = self.cred.get_credentials(self.service, self.username)

        connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                            f'SERVER={self.server};'
                            f'DATABASE={self.database};'
                            f'UID={self.username};'
                            f'PWD={password};'
                            )

        #Set up pyodbc connection
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

        #Set up sqlalchemy engine
        params = urllib.parse.quote_plus(connection_string)
        sqlalchemy_database_url = "mssql+pyodbc:///?odbc_connect={}".format(params)
        self.sqlalchemy_engine = create_engine(sqlalchemy_database_url)

    def add_new_dataframe(self, table, dataframe):
        """Add meta data to a table in the database.

        Args:
            table: Table for storing data
            dataframe (pandas.DataFrame): Containing meta data for storage.
        """
        dataframe.to_sql(table, self.sqlalchemy_engine, if_exists='append', index=False)




