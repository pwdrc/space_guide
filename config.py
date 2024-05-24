# Description: Configuration file for the application.
# The configuration file contains the connection information for the Oracle database.
import getpass

class AccessConfig:
    ORACLE_USER = None
    ORACLE_PASSWORD = None
    ORACLE_DSN = "orclgrad1.icmc.usp.br:1521/pdb_elaine.icmc.usp.br"

    def get_db_credentials(self):
        self.ORACLE_USER = input("Enter the Oracle username: ")
        self.ORACLE_PASSWORD = getpass.getpass("Enter the Oracle password: ")