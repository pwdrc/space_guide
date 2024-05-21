import cx_Oracle as oracledb
from config import Config

class UserDAO:
    def __init__(self):
        self.connection = oracledb.connect(Config.ORACLE_USER, Config.ORACLE_PASSWORD, Config.ORACLE_DSN)
