import socket
import asyncio
import time
import random
import json

from mysql.connector import connection
from mysql.connector import errorcode

from walkoff_app_sdk.app_base import AppBase

class DbManager(AppBase):
    __version__ = "1.0.0"
    app_name = "SF-DBManager"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def connection(self, username, password, host, port, database_name):
        cnx = connection.MySQLConnection(user=username, password= password,
                                        host= host,
                                        port=port,
                                        database= database_name)
        print(f"Connection successful, User -->{username} ")                                
        return cnx                               

    def query_mysql_database(self, username, password, host, port, database_name, query):
        
        self.db_connection = self.connection(username, password, host, port, database_name) 
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            cursor.execute(str(query))
        except:
            res = {}
            res["ERROR"] = "erro na syntaxe da query"
            res["query"] = str(query)
        print("Query executed successfully")
        res = cursor.fetchall()
        cursor.close()
        self.db_connection.close()
        try:
            res1 = json.dumps(res)
            res2 = res
        except:
            res2 = {}
            res = str(res).replace("{", "\t")
            res = str(res).replace("}", "\t")
            res = str(res).replace('"', "")
            res2["res1message"] = str(res)
        if res2:
            return (json.dumps(res2))
        else:
            return(json.dumps(res))

if __name__ == "__main__":
    DbManager.run()
