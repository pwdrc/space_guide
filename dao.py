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
        self.create_table_users()
        self.create_log_table()
    
# criada uma tabela chamada USERS, para armazenar os usuários do sistema, com os
# seguintes atributos: Userid (ID sintético), Password, IdLider (id na tabela de origem - Lider). A
# chave primária deve ser Userid, e o atributo IdLider deve ser único, referenciando a tabela de
# líderes. O atributo Password deve utilizar a função md5 do SGBD para armazenar os dados.
# Os líderes já cadastrados na base deverão ser cadastrados manualmente na tabela USERS, i.e.,
# deve ser criado um procedimento (PL/SQL) para encontrar líderes sem respectivas tuplas na tabela
# USERS e inserí-los com uma senha padrão. O procedimento pode ser executado manualmente,
# via SQL Developer. Além disso, deve ser criada uma tabela chamada LOG_TABLE para
# armazenar o log de acessos e operações dos usuários do sistema, com os seguintes atributos:
# Userid (associado à table a USERS), timestamp, message. A tabela de logs deverá ser mantida
# por chamadas da aplicação.     

    def fill_table_users(self):
        # criar um procedimento (PL/SQL) para encontrar líderes sem respectivas tuplas na tabela USERS e inserí-los com uma senha padrão
        # o procedimento pode ser executado manualmente, via SQL Developer
        # Userid é um id sintetico
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USERS (Userid, Password, IdLider)
                SELECT DBMS_RANDOM.VALUE(1000, 9999), standard_hash('123456', 'MD5'), Lider.CPI
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

                    try:
                        print("Preenchendo tabela USERS...")
                        self.fill_table_users()
                        print("Tabela USERS preenchida com sucesso!")
                    except oracledb.DatabaseError as e:
                        print(f"Falha no preenchimento da tabela USERS: {e.args[0].message}")                    
            except oracledb.DatabaseError as e:
                print(f"Falha na criação da USERS (tabela): {e.args[0].message}")
        else:
            print("Tabela USERS já existe! Continuando...")

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