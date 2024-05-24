# Description: This file contains the services for the user.
# The services are responsible for handling the business logic of the application.
# The services interact with the DAO classes to access the database.

from dao import DataBaseActions
import hashlib
import oracledb

class SpaceGuideServices:
    def __init__(self):
        self.service = DataBaseActions()

    def init_environment(self):
        try:
            print(f"Configurando a base de dados...")
            self.service.create_table_users()
            self.service.create_log_table()
        except oracledb.DatabaseError as e:
            print(f"Erro ao configurar a base de dados: {e.args[0].message}")
            exit(1)
               
    def login(self, username, password):
        user_info = self.service.get_login_info(username)
        if user_info is None:
            return False

        hashed_password = hashlib.md5(password.encode()).hexdigest().upper()
        if user_info[1] == hashed_password:
            return True

        return False
        
    def set_url(self, role):
        if role == "COMANDANTE":
            return "/commander"
        if role == "OFICIAL":
            return "/officer"
        if role == "CIENTISTA":
            return "/scientist"
        return "/leader"