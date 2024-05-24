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
        
    def get_role(self, userid):
        CPI = self.service.get_CPI_by_userid(userid)
        print(f">>>>> CPI: {CPI}")
        if self.service.is_user_a_faction_leader(CPI):
            return 'LIDER_FACCAO'

        role = self.service.get_role_by_CPI(CPI).strip()
        print(f">>>>> Role: {role}")
        return role
        