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

    def remove_dataframe(self,table,primary_keys):
        """Remove metadata from a table in the database

        Args:
            table (string): table name
            primary key (int list): list of all primary keys to be removed
        """
        for primary_key in primary_keys:
            print('deleting', primary_key)
            #self.cursor.execute(f'DELETE FROM {table} WHERE movie_id='{primary_key}';')
            self.cursor.execute(f'DELETE FROM movie_data WHERE movie_id={primary_key};')
            self.connection.commit()
        
    def search_database(self,search_dict):
        """Function that search the database and returns records fullfilling
        the recuirment specified in the search_dict. All clause are added with 
        the AND-operator, thus all must be fullfiled at the same time. 
        To specify a time of recoring specify an "upper time" and a "lower time"
        in the dict on the form "yyyy-mm-dd hh:mm:ss".

        Args:
            search_dict (dict): Column and values to be added in where clause

        Returns:
            list,list: list of movie ids and movie names that where found
        """
        
        # construct query string
        query_string = 'SELECT movie_id, movie_file_path FROM movie_data WHERE '
        clause=0
        if 'lower time' in search_dict and 'upper time' in search_dict:
            query_string+= f"record_time BETWEEN \'{search_dict['lower time']}\' AND \'{search_dict['upper time']}\'"
            clause+=1
        for key in search_dict.keys():
            if key=='upper time' or key=='lower time':
                continue
            elif clause>0:
                query_string+=' AND '
            query_string += f'{key}=\'{search_dict[key]}\''
            clause+=1
        query_string+=';'
        
        # Execute query and get result
        self.cursor.execute(query_string)
        rows = self.cursor.fetchall()
        movie_id=[]
        movie_name=[]
        for row in rows:
            movie_id.append(row[0])
            movie_name.append(row[1])
            
        return movie_id, movie_name


