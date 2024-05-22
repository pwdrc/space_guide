# Description: Configuration file for the application.
# The configuration file contains the connection information for the Oracle database.

class AccessConfig:
    # default
    ORACLE_USER = None
    ORACLE_PASSWORD = None
    ORACLE_DSN = "orclgrad1.icmc.usp.br:1521/pdb_elaine.icmc.usp.br"

    def get_credentials(self):
        self.ORACLE_USER = input("Digite o usuário do banco de dados: ")
        self.ORACLE_PASSWORD = input("Digite a senha do banco de dados: ")
