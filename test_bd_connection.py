import getpass
import oracledb

user = 'a10492012'
password = 'a10492012'
dsn = 'orclgrad1.icmc.usp.br:1521/pdb_elaine.icmc.usp.br'

with oracledb.connect(user=user, password=password, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM planeta"
        for r in cursor.execute(sql):
            print(r)