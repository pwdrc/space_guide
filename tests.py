# from dao import DataBaseActions as db

# test = db()
# sql = "SELECT * FROM planeta"
# test.select(sql)

# test user get_role
from services import SpaceGuideServices as sv
test_get_role = sv()
print(test_get_role.get_role(5746)) # should return 'LIDER_FACCAO'
print(test_get_role.get_role(8948)) # should return 'OFICIAL'
print(test_get_role.get_role(1010)) # should return 'ZEH_NGM'