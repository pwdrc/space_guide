# Description: This file contains the services for the user.
# The services are responsible for handling the business logic of the application.
# The services interact with the DAO classes to access the database.

from dao import UserDAO

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()