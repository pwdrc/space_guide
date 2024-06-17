import oracledb
import config

class OracleDBInitializer:
    def __init__(self, user, password, dsn):
        self.connection = oracledb.connect(user=user, password=password, dsn=dsn)
    
    def procedure_exists(self, procedure_name):
        query = """
            SELECT COUNT(*)
            FROM USER_PROCEDURES
            WHERE OBJECT_NAME = UPPER(:procedure_name)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, {'procedure_name': procedure_name})
            result = cursor.fetchone()
            return result[0] > 0
        
    def table_exists(self, table_name):
        try:
            with self.connection.cursor() as cursor:
                p_exists = cursor.var(oracledb.NUMBER)
                cursor.callproc('PRC_TABLE_EXISTS', [table_name, p_exists])
                return p_exists.getvalue() > 0
        except oracledb.DatabaseError as e:
            print(f"Erro ao verificar existência da tabela: {e}")
            return False
    
    def create_procedures_and_functions(self):
        try:
            with self.connection.cursor() as cursor:
                # Cria PRC_TABLE_EXISTS
                if not self.procedure_exists('PRC_TABLE_EXISTS'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_TABLE_EXISTS(p_table_name IN VARCHAR2, p_exists OUT NUMBER) AS
                        BEGIN
                            SELECT COUNT(*)
                            INTO p_exists
                            FROM USER_TABLES
                            WHERE TABLE_NAME = UPPER(p_table_name);
                        END;
                    """)
                    print("Procedimento PRC_TABLE_EXISTS criado.")
                else:
                    print("Procedimento PRC_TABLE_EXISTS já existe. Pulando criação.")
                    
                # Cria USERS table
                if not self.procedure_exists('PRC_CREATE_TABLE_USERS'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_CREATE_TABLE_USERS AS 
                        BEGIN
                            EXECUTE IMMEDIATE '
                            CREATE TABLE USERS (
                                Userid NUMBER PRIMARY KEY,
                                Password VARCHAR2(32), 
                                IdLider CHAR(14) UNIQUE,
                                CONSTRAINT FK_USERS_TABLE_SG FOREIGN KEY (IdLider) REFERENCES Lider(CPI) ON DELETE CASCADE
                            )';
                            COMMIT;
                        EXCEPTION
                            WHEN OTHERS THEN
                                IF SQLCODE = -955 THEN
                                    NULL; -- Table already exists
                                ELSE
                                    RAISE;
                                END IF;
                        END;
                    """)
                    print("Procedimento PRC_CREATE_TABLE_USERS criado.")
                else:
                    print("Procedimento PRC_CREATE_TABLE_USERS já existe. Pulando criação.")

                # Procedimento para preencher tabela USERS
                if not self.procedure_exists('PRC_FILL_TABLE_USERS'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_FILL_TABLE_USERS AS 
                        BEGIN
                            INSERT INTO USERS (Userid, Password, IdLider)
                            SELECT round(DBMS_RANDOM.VALUE(1000, 9999)), standard_hash('123456', 'MD5'), Lider.CPI
                            FROM Lider
                            WHERE Lider.CPI NOT IN (SELECT IdLider FROM USERS);
                            COMMIT;
                        END;
                    """)
                    print("Procedimento PRC_FILL_TABLE_USERS criado.")
                else:
                    print("Procedimento PRC_FILL_TABLE_USERS já existe. Pulando criação.")

                # Procedimento para criar tabela LOG_TABLE
                if not self.procedure_exists('PRC_CREATE_LOG_TABLE'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_CREATE_LOG_TABLE AS 
                        BEGIN
                            EXECUTE IMMEDIATE '
                            CREATE TABLE LOG_TABLE (
                                Userid NUMBER,
                                Timestamp TIMESTAMP,
                                Message VARCHAR2(255),
                                CONSTRAINT FK_LOG_TABLE_SG FOREIGN KEY (Userid) REFERENCES USERS(Userid) ON DELETE CASCADE
                            )';
                            COMMIT;
                        EXCEPTION
                            WHEN OTHERS THEN
                                IF SQLCODE = -955 THEN
                                    NULL; -- Table already exists
                                ELSE
                                    RAISE;
                                END IF;
                        END;
                    """)
                    print("Procedimento PRC_CREATE_LOG_TABLE criado.")
                else:
                    print("Procedimento PRC_CREATE_LOG_TABLE já existe. Pulando criação.")

                # Procedimento para inserir log
                if not self.procedure_exists('PRC_INSERT_LOG'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_INSERT_LOG(p_user_id NUMBER, p_message VARCHAR2) AS 
                        BEGIN
                            INSERT INTO LOG_TABLE (Userid, Timestamp, Message)
                            VALUES (p_user_id, SYSTIMESTAMP, p_message);
                            COMMIT;
                        END;
                    """)
                    print("Procedimento PRC_INSERT_LOG criado.")
                else:
                    print("Procedimento PRC_INSERT_LOG já existe. Pulando criação.")

                # Procedimento para obter informações de login
                if not self.procedure_exists('PRC_GET_LOGIN_INFO'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_LOGIN_INFO(p_username NUMBER) AS 
                            v_cursor SYS_REFCURSOR;
                        BEGIN
                            OPEN v_cursor FOR
                            SELECT *
                            FROM USERS
                            WHERE UserId = p_username;
                        END;
                    """)
                    print("Procedimento PRC_GET_LOGIN_INFO criado.")
                else:
                    print("Procedimento PRC_GET_LOGIN_INFO já existe. Pulando criação.")

                # Procedimento para obter cargo pelo CPI
                if not self.procedure_exists('PRC_GET_ROLE_BY_CPI'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_ROLE_BY_CPI(p_CPI CHAR) AS 
                            v_role VARCHAR2(255);
                        BEGIN
                            SELECT Cargo INTO v_role
                            FROM Lider
                            WHERE CPI = p_CPI;
                        EXCEPTION
                            WHEN NO_DATA_FOUND THEN
                                v_role := 'ZEH_NGM';
                        END;
                    """)
                    print("Procedimento PRC_GET_ROLE_BY_CPI criado.")
                else:
                    print("Procedimento PRC_GET_ROLE_BY_CPI já existe. Pulando criação.")

                # Procedimento para obter CPI pelo User ID
                if not self.procedure_exists('PRC_GET_CPI_BY_USERID'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_CPI_BY_USERID(p_userid NUMBER) AS 
                            v_CPI CHAR(14);
                        BEGIN
                            SELECT Lider.CPI INTO v_CPI
                            FROM Lider
                            JOIN USERS
                            ON USERS.IdLider = Lider.CPI
                            WHERE USERS.Userid = p_userid;
                        EXCEPTION
                            WHEN NO_DATA_FOUND THEN
                                v_CPI := NULL;
                        END;
                    """)
                    print("Procedimento PRC_GET_CPI_BY_USERID criado.")
                else:
                    print("Procedimento PRC_GET_CPI_BY_USERID já existe. Pulando criação.")

                # Procedimento para obter nome pelo User ID
                if not self.procedure_exists('PRC_GET_NAME_BY_USERID'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_NAME_BY_USERID(p_CPI CHAR) AS 
                            v_name VARCHAR2(255);
                        BEGIN
                            SELECT nome INTO v_name
                            FROM Lider
                            WHERE CPI = p_CPI;
                        EXCEPTION
                            WHEN NO_DATA_FOUND THEN
                                v_name := NULL;
                        END;
                    """)
                    print("Procedimento PRC_GET_NAME_BY_USERID criado.")
                else:
                    print("Procedimento PRC_GET_NAME_BY_USERID já existe. Pulando criação.")

                # Procedimento para obter facção pelo User ID
                if not self.procedure_exists('PRC_GET_FACCAO_BY_USERID'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_FACCAO_BY_USERID(p_CPI CHAR) AS 
                            v_faccao VARCHAR2(255);
                        BEGIN
                            SELECT nome INTO v_faccao
                            FROM faccao
                            WHERE lider = p_CPI;
                        EXCEPTION
                            WHEN NO_DATA_FOUND THEN
                                v_faccao := NULL;
                        END;
                    """)
                    print("Procedimento PRC_GET_FACCAO_BY_USERID criado.")
                else:
                    print("Procedimento PRC_GET_FACCAO_BY_USERID já existe. Pulando criação.")

                # Procedimento para obter nação pelo User ID
                if not self.procedure_exists('PRC_GET_NACAO_BY_USERID'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_GET_NACAO_BY_USERID(p_CPI CHAR) AS 
                            v_nacao VARCHAR2(255);
                        BEGIN
                            SELECT nacao INTO v_nacao
                            FROM lider
                            WHERE CPI = p_CPI;
                        EXCEPTION
                            WHEN NO_DATA_FOUND THEN
                                v_nacao := NULL;
                        END;
                    """)
                    print("Procedimento PRC_GET_NACAO_BY_USERID criado.")
                else:
                    print("Procedimento PRC_GET_NACAO_BY_USERID já existe. Pulando criação.")

                # Procedimento para verificar se usuário é líder de facção
                if not self.procedure_exists('PRC_IS_USER_A_FACTION_LEADER'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_IS_USER_A_FACTION_LEADER(p_CPI CHAR) AS 
                            v_count NUMBER;
                        BEGIN
                            SELECT COUNT(*) INTO v_count
                            FROM faccao
                            WHERE lider = p_CPI;
                                   END;
    """)
                    print("Procedimento PRC_IS_USER_A_FACTION_LEADER criado.")
                else:
                    print("Procedimento PRC_IS_USER_A_FACTION_LEADER já existe. Pulando criação.")

                if not self.procedure_exists('PRC_SELECT_DATA'):
                    cursor.execute("""
                        CREATE OR REPLACE PROCEDURE PRC_SELECT_DATA(p_query VARCHAR2, p_cursor OUT SYS_REFCURSOR) AS 
                        BEGIN
                            OPEN p_cursor FOR p_query;
                        END;
                    """)
                    print("Procedimento PRC_SELECT_DATA criado.")
                else:
                    print("Procedimento PRC_SELECT_DATA já existe. Pulando criação.")

        except oracledb.DatabaseError as e:
            print(f"Erro ao criar procedimentos e funções: {e}")
        finally:
            self.connection.close()

if __name__ == "__main__":
    access_config = config.AccessConfig()
    access_config.get_db_credentials()
    initializer = OracleDBInitializer(access_config.ORACLE_USER, access_config.ORACLE_PASSWORD, access_config.ORACLE_DSN)
    initializer.create_procedures_and_functions()
