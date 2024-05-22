from dao import DataBaseActions as db

test = db()
sql = "SELECT * FROM planeta"
test.select(sql)