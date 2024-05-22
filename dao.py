# Description: This file contains the DAO classes for the application.
# The DAO classes are responsible for handling the database connections and queries.

from config import AccessConfig
import oracledb

class DataBaseActions:
    def __init__(self):
        self.connection = oracledb.connect(
            user=AccessConfig.ORACLE_USER,
            password=AccessConfig.ORACLE_PASSWORD,
            dsn=AccessConfig.ORACLE_DSN
        )
    
    def select(self, sql):
        with self.connection.cursor() as cursor:
            for r in cursor.execute(sql):
                print(r)