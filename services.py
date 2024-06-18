import logging
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
               
#########################################################
# Funções de acesso ao banco de dados e regras de negócio
#########################################################

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
        faccao = self.service.get_faccao_by_userid(userid)
        if faccao is not None:
            faccao = faccao.strip()
        else:
            faccao = ""
        print(f">>>>> Faccao: {faccao}")
        return faccao
    
    def get_nacao(self, userid):
        nacao = self.service.get_nacao_by_userid(userid).strip()
        print(f">>>>> Nacao: {nacao}")
        return nacao
    
    # def register_access(self, userid, message):
    #     self.service.insert_log(userid, message)
    #     print(">>>>> Log gravado com sucesso!")

    
    def register_access(self, username, message):
        # Verifique se o usuário existe antes de inserir o log
        if self.service.get_login_info(username) is not None:
            # Chame o método de inserção de log
            self.service.insert_log(username, message)

    def is_leader(self, userid):
        CPI = self.service.get_CPI_by_userid(userid)
        return self.service.is_user_a_faction_leader(CPI)
    
    #########################################################
    # LIDER
    #########################################################
    
    def update_faccao(self, userid, novo_nome):
        self.service.Alterar_Nome_Faccao(userid, novo_nome)

    def update_lider(self, userid, CPI_novo_lider):
        self.service.Indicar_Novo_Lider(userid, CPI_novo_lider)
    
    def add_comunidade(self, userid, especie, comunidade):
        self.service.Credencia_Comunidade(userid, especie, comunidade)

    def rm_nacao(self, userid, nacao):
        self.service.Remove_Faccao_Naccao(userid, nacao)

    def relatorio_comunidades(self, userid):
        return self.service.Relatorio_Comunidades(userid)
    
    #########################################################
    # COMANDANTE
    #########################################################

    def add_nacao_federacao(self, userid, Federacao):
        self.service.Insere_Nacao_Federacao(userid, Federacao)
    
    def rm_nacao_federacao(self, userid):
        self.service.Remove_Nacao_Federacao(userid)

    def criar_nacao_federacao(self, userid, Federacao):
        self.service.Cria_Nacao_Com_Federacao(userid, Federacao)
    
    def add_dominancia(self, userid, planeta):
        self.service.Insere_Nova_Dominancia(userid, planeta)
    
    def relatorio_nacoes(self, userid):
        return self.service.Relatorio_Nacoes_Participa(userid)

    def relatorio_planetas_potenciais(self, userid, DIST_MAX):
        return self.service.Planetas_Ponteciais(userid, DIST_MAX)
    
    #########################################################
    # CIENTISTA
    #########################################################

    def add_estrela(self,ID,Nome,Classificao,Massa,X,Y,Z):
        self.service.Cria_Estrela(ID,Nome,Classificao,Massa,X,Y,Z)

    def add_sistema(self,Estrela,Nome):
        self.service.Cria_Sistema(Estrela,Nome)
    
    def add_orbita_estrela(self,Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo):
        self.service.Cria_Oribta_Estrela(Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo)
    
    def relatorio_estrela_sem_classificacao(self):
        return self.service.Estrelas_Sem_Classificao()
    
    def relatorio_planeta_sem_classificacao(self):
        return self.service.Planetas_Sem_Classificao()
        