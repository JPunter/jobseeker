''' Interacts with postgreSQL

'''

import psycopg2
import pandas
import sys
from sqlalchemy import create_engine


class PostGresTools:
    #initialise the object by creating the engine and connecting
    def __init__(self,dbname,user,host,password):
        self.dbname = dbname
        self.dbuser = user
        self.dbhost = host
        self.dbpass = password

        try:
            self.engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:5432/{3}".format(self.dbuser,
            self.dbpass,self.dbhost,self.dbname))
            print("Database engine established")
        except:
            print("Could not establish database engine, exiting program.")
            sys.exit()
        
        try:
            self.conn = self.engine.connect().connection
            print("Database connection established\n")
        except:
            print("Could not establish database connection, exiting program.")
            sys.exit()
        
    
    #writes to table within preconnected database
    def writeTable(self, data, table_name):
        try:
            data.to_sql(table_name, self.engine, schema="public",
            if_exists="append", index=False)
        except:
            print("Could not write to table")
    
    #query table
    def query(self, query):
        return pandas.read_sql_query(query, con=self.conn)
