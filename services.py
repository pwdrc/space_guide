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
        role = self.service.get_role_by_CPI(CPI).strip()
        print(f">>>>> Role: {role}")
        return role
    
    def get_name(self, userid):
        name = self.service.get_name_by_userid(userid).strip()
        print(f">>>>> Name: {name}")
        return name
    
    def get_faccao(self, userid):
        faccao = self.service.get_faccao_by_userid(userid).strip()
        print(f">>>>> Faccao: {faccao}")
        return faccao
    
    def get_nacao(self, userid):
        nacao = self.service.get_nacao_by_userid(userid).strip()
        print(f">>>>> Nacao: {nacao}")
        return nacao
    
    def register_access(self, userid, message):
        self.service.insert_log(userid, message)
        print(">>>>> Log gravado com sucesso!")

    def is_leader(self, userid):
        CPI = self.service.get_CPI_by_userid(userid)
        return self.service.is_user_a_faction_leader(CPI)
    
    def update_faccao(self, oldname, newname):
        self.service.alterar_nome_faccao(oldname, newname)
        print(">>>>> Nome da Faccao atualizado com sucesso!")