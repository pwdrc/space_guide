from dao import UserDAO

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()