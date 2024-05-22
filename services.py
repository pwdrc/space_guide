# Description: This file contains the services for the user.
# The services are responsible for handling the business logic of the application.
# The services interact with the DAO classes to access the database.

from dao import DataBaseActions

class SpaceGuideServices:
    def __init__(self):
        self.service = DataBaseActions()
        self.on = False

    def init_environment(self):
        if not self.on: 
        print(f"Configurando a base de dados...")
        self.service.create_table_users()
        self.service.create_table_log_table()
        self.on = True
        