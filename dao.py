from config import AccessConfig
import oracledb

class DataBaseActions:
    def __init__(self):
        self.config = AccessConfig()
        self.config.get_db_credentials()
        try:
            self.connection = oracledb.connect(
                user=self.config.ORACLE_USER,
                password=self.config.ORACLE_PASSWORD,
                dsn=self.config.ORACLE_DSN
            )
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao banco de dados: {e.args[0].message}")
            exit(1)

######################################################################
########### funcoes de oficial #######################################

    def Relatorio_Habitacao(self,userid):
            with self.connection.cursor() as cursor:
                CPI = self.get_CPI_by_userid(userid)
                chunk_size = 100
                query = 'Oficial.relatorio_habitantes'            
                try:
                    cursor.callproc("dbms_output.enable")
                    print("Planeta      Comunidade      QTD_Habitantes      Data_Ini\n")
                    cursor.callproc(query,(CPI,))
                    lines_var = cursor.arrayvar(str, chunk_size)
                    num_lines_var = cursor.var(int)
                    num_lines_var.setvalue(0, chunk_size)
                    while True:
                        cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                        num_lines = num_lines_var.getvalue()
                        lines = lines_var.getvalue()[:num_lines]
                        for line in lines:
                            print(line or "")
                        if num_lines < chunk_size:
                            break
                except oracledb.IntegrityError as e:        
                    error_obj, = e.args
                    print(error_obj.message)
                self.connection.commit()

######################################################################
########### funções lider faccao #####################################

#       Funcao a.i
    def Alterar_Nome_Faccao(self, userid, NomeNovo):
        with self.connection.cursor() as cursor:
            NomeAntigo = self.get_faccao_by_userid(userid)
            query = 'pacote_lider.alterar_nome_faccao'
            try:
                cursor.callproc(query,(NomeAntigo,NomeNovo))
            except oracledb.IntegrityError as e:   
                print(e)
            else:
                print("Alteracao realizada com sucesso")
            self.connection.commit()

    #       Funcao a.ii
    def Indicar_Novo_Lider(self,userid,CPI_Novo):
        with self.connection.cursor() as cursor:
            CPI = self.get_CPI_by_userid(userid)
            query = 'Pacote_Lider.indicar_novo_lider'
            try:
                cursor.callproc(query,(CPI,CPI_Novo))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)
            else:
                print("O novo lider foi indicado com sucesso")    
            self.connection.commit()
    
    #       Funcao a.iii
    def Credencia_Comunidade(self,userid,Especie,Comunidade):
        with self.connection.cursor() as cursor:
            Faccao = self.get_faccao_by_userid(userid)
            query = 'Pacote_Lider.lider_insere_pariticipa'
            try:
                cursor.callproc(query,(Faccao,Especie,Comunidade))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)
            else:
                print("A Comunidade foi credenciada com sucesso")    

            self.connection.commit()

    #       Funcao b
    def Remove_Faccao_Naccao(self,userid,Nacao):
        with self.connection.cursor() as cursor:
            Faccao = self.get_faccao_by_userid(userid)
            query = 'Pacote_Lider.remover_faccao_de_nacao'
            try:
                cursor.callproc(query,(Faccao,Nacao))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)
            else:
                print("A Faccao foi removida da Nacao com sucesso")    
            self.connection.commit()


    #       Relatorios a.i
    def Relatorio_Comunidades(self,userid):
        with self.connection.cursor() as cursor:
            Faccao = self.get_faccao_by_userid(userid)
            chunk_size = 100
            query = 'Pacote_Lider.relatorio_comunidades'
            try:
                cursor.callproc("dbms_output.enable")
                print("Planeta      Comunidade      Especie      QTD_Habitantes     Nacao      Data_Ini\n")
                cursor.callproc(query,(Faccao,))
                lines_var = cursor.arrayvar(str, chunk_size)
                num_lines_var = cursor.var(int)
                num_lines_var.setvalue(0, chunk_size)
                while True:
                    cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                    num_lines = num_lines_var.getvalue()
                    lines = lines_var.getvalue()[:num_lines]
                    for line in lines:
                        print(line or "")
                    if num_lines < chunk_size:
                        break
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)  
            self.connection.commit()


####################################################################################
########### funções comandante #####################################################

    #       Funcao a.i.1
    def Insere_Nacao_Federacao(self,userid,Federacao):
        with self.connection.cursor() as cursor:
            #marcador de transacao
            self.connection.begin() 
            query = 'Comandante.insere_federacao'
            try:    
                Nacao = self.get_nacao_by_userid(userid)
                cursor.callproc(query,(Nacao,Federacao))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Insercao Completa com sucesso') 
            #finalizacao de transacao
            self.connection.commit()

    #       Funcao a.i.2
    def Remove_Nacao_Federacao(self,userid):
        with self.connection.cursor() as cursor:
            #marcador de transacao
            self.connection.begin() 
            query = 'Comandante.exclui_federacao'
            try:    
                Nacao = self.get_nacao_by_userid(userid)
                cursor.callproc(query,(Nacao,))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Remocao Completa com sucesso') 
            #finalizacao de transacao
            self.connection.commit()

    #       Funcao a.ii
    def Cria_Nacao_Com_Federacao(self,userid,Federacao):
        with self.connection.cursor() as cursor:
            query = 'Comandante.cria_federacao'
            try:    
                Nacao = self.get_nacao_by_userid(userid)
                cursor.callproc(query,(Nacao,Federacao))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Criacao Completa com sucesso') 
            self.connection.commit()

    #       Funcao b
    def Insere_Nova_Dominancia(self,userid,Planeta):
        with self.connection.cursor() as cursor:
            query = 'Comandante.nova_dominancia'
            try:    
                Nacao = self.get_nacao_by_userid(userid)
                cursor.callproc(query,(Nacao,Planeta))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Insercao Completa com sucesso') 
            self.connection.commit()

    #       Relatorio a.i
    def Relatorio_Nacoes_Participa(self,userid):
        with self.connection.cursor() as cursor:
            Faccao = self.get_faccao_by_userid(userid)
            chunk_size = 100
            query = 'Comandante.recupera_informacoes'
            try:
                cursor.callproc("dbms_output.enable")
                print("Planeta      Especie      Inteligente     Comunidade     Qtd_Habitantes      Faccao\n")
                cursor.callproc(query,(Faccao,))
                lines_var = cursor.arrayvar(str, chunk_size)
                num_lines_var = cursor.var(int)
                num_lines_var.setvalue(0, chunk_size)
                while True:
                    cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                    num_lines = num_lines_var.getvalue()
                    lines = lines_var.getvalue()[:num_lines]
                    for line in lines:
                        print(line or "")
                    if num_lines < chunk_size:
                        break
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)  
            self.connection.commit()
    
    #       Relatorio a.ii
    def Planetas_Ponteciais(self, userid,  DIST_MAX):
        with self.connection.cursor() as cursor:
            CPI = self.get_CPI_by_userid(userid)
            DIST_MAX = 100
            chunk_size = 100
            query = 'comandante.planetas_pontenciais'
            try:
                cursor.callproc("dbms_output.enable")
                print("ID_Astro                 Raio     Habitacoes          Dist_Nacao\n")
                cursor.callproc(query,(CPI,DIST_MAX))
                lines_var = cursor.arrayvar(str, chunk_size)
                num_lines_var = cursor.var(int)
                num_lines_var.setvalue(0, chunk_size)
                while True:
                    cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                    num_lines = num_lines_var.getvalue()
                    lines = lines_var.getvalue()[:num_lines]
                    for line in lines:
                        print(line or "")
                    if num_lines < chunk_size:
                        break
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)  
            self.connection.commit()


####################################################################################
########### funções cientista ######################################################

    #       Funcao a.1
    def Cria_Estrela(self,ID,Nome,Classificao,Massa,X,Y,Z):
        with self.connection.cursor() as cursor:
            query = 'cientista.cria_estrela'
            try:    
                cursor.callproc(query,(ID,Nome,Classificao,Massa,X,Y,Z))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Estrela criada com sucesso') 
            self.connection.commit()

    #       Funcao a.2
    def Cria_Sistema(self,Estrela,Nome):
        with self.connection.cursor() as cursor:
            query = 'cientista.cria_sistema'
            try:    
                cursor.callproc(query,(Estrela,Nome))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Sistema criado com sucesso') 
            self.connection.commit()

    #       Funcao a.3
    def Cria_Oribta_Estrela(self,Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo):    
        with self.connection.cursor() as cursor:
            query = 'cientista.cria_orbitaestrela'
            try:    
                cursor.callproc(query,(Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo))
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message) 
            else:
                print('Orbita criada com sucesso') 
            self.connection.commit()

    #       Relatorio a.i
    def Estrelas_Sem_Classificao(self):
        with self.connection.cursor() as cursor:
            chunk_size = 100
            query = 'cientista.estrela_nao_classificada'
            try:
                cursor.callproc("dbms_output.enable")
                print("ID_Estrela            Massa                      x                y               z\n")
                cursor.callproc(query)
                lines_var = cursor.arrayvar(str, chunk_size)
                num_lines_var = cursor.var(int)
                num_lines_var.setvalue(0, chunk_size)
                while True:
                    cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                    num_lines = num_lines_var.getvalue()
                    lines = lines_var.getvalue()[:num_lines]
                    for line in lines:
                        print(line or "")
                    if num_lines < chunk_size:
                        break
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)  
            self.connection.commit()

    #       Relatorio a.ii
    def Planetas_Sem_Classificao(self):
        with self.connection.cursor() as cursor:
            chunk_size = 100
            query = 'cientista.planeta_nao_classificado'
            try:
                cursor.callproc("dbms_output.enable")
                print("ID_Astro           Massa         Raio\n")
                cursor.callproc(query)
                lines_var = cursor.arrayvar(str, chunk_size)
                num_lines_var = cursor.var(int)
                num_lines_var.setvalue(0, chunk_size)
                while True:
                    cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                    num_lines = num_lines_var.getvalue()
                    lines = lines_var.getvalue()[:num_lines]
                    for line in lines:
                        print(line or "")
                    if num_lines < chunk_size:
                        break
            except oracledb.IntegrityError as e:
                error_obj, = e.args
                print(error_obj.message)  
            self.connection.commit()


########### funções gerais de gerencia de login #####################################
    

    def fill_table_users(self):
        # criar um procedimento (PL/SQL) para encontrar líderes sem respectivas tuplas na tabela USERS e inserí-los com uma senha padrão
        # o procedimento pode ser executado manualmente, via SQL Developer
        # Userid é um id sintetico
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USERS (Userid, Password, IdLider)
                SELECT round(DBMS_RANDOM.VALUE(1000, 9999)), standard_hash('123456', 'MD5'), Lider.CPI
                FROM Lider
                WHERE Lider.CPI NOT IN (SELECT IdLider FROM USERS)
            """)
            print("Tabela USERS preenchida com sucesso!")

    def create_table_users(self):
        # se a tabela ainda nao existir, criar
        # se existir, informar que a tabela ja existe
        # usar a funcao md5 do SGBD para armazenar os dados
        # MD5 hash tem 32 caracteres hexadecimais
        if not self.table_exists('USERS'):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE USERS (
                            Userid NUMBER PRIMARY KEY,
                            Password VARCHAR2(32), 
                            IdLider CHAR(14) UNIQUE,
                            CONSTRAINT FK_USERS_TABLE_SG FOREIGN KEY (IdLider) REFERENCES Lider(CPI) ON DELETE CASCADE
                        )
                    """)
                    print("Tabela USERS criada com sucesso!")
                   
            except oracledb.DatabaseError as e:
                print(f"Falha na criação da USERS (tabela): {e.args[0].message}")
        else:
            print("Tabela USERS já existe! Continuando...")

        try:
            self.fill_table_users()
        except oracledb.DatabaseError as e:
            print(f"Falha no preenchimento da tabela USERS: {e.args[0].message}")
    
    def create_log_table(self):
        # se a tabela ainda nao existir, criar
        # se existir, informar que a tabela ja existe
        if not self.table_exists('LOG_TABLE'):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE LOG_TABLE (
                            Userid NUMBER,
                            Timestamp TIMESTAMP,
                            Message VARCHAR2(255),
                            CONSTRAINT FK_LOG_TABLE_SG FOREIGN KEY (Userid) REFERENCES USERS(Userid) ON DELETE CASCADE
                        )
                    """)
                    print("Tabela LOG_TABLE criada com sucesso!")
            except oracledb.DatabaseError as e:
                print(f"Falha na criação da LOG_TABLE: {e.args[0].message}")
        else:
            print("Tabela LOG_TABLE já existe! Continuando...")
    
    def insert_log(self, user_id, message):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO LOG_TABLE (Userid, Timestamp, Message)
                VALUES (:user_id, SYSTIMESTAMP, :message)
            """, user_id=user_id, message=message)
            print("Log inserido com sucesso!")
    
    def table_exists(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM USER_TABLES
                WHERE TABLE_NAME = UPPER(:table_name)
            """, {'table_name': table_name})
            result = cursor.fetchone()
            return result[0] > 0

    def select(self, sql):
        with self.connection.cursor() as cursor:
            for r in cursor.execute(sql):
                print(r)

    def get_login_info(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM USERS
                WHERE UserId = :username
            """, username=username)
            return cursor.fetchone()
    
    def get_role_by_CPI(self, CPI):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT Cargo
                FROM Lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else 'ZEH_NGM'
        
    def get_CPI_by_userid(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT Lider.CPI
                FROM Lider
                JOIN USERS
                ON USERS.IdLider = Lider.CPI
                WHERE USERS.Userid = :userid
            """, userid=userid)
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_name_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome
                FROM Lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_faccao_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome
                FROM faccao
                WHERE lider = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_nacao_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nacao
                FROM lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
    
    def is_user_a_faction_leader(self, CPI):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM faccao
                WHERE lider = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] > 0