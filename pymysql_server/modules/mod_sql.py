import pymysql

class Database():
    def __init__(self):
        self._db = pymysql.connect(
        user = "root",
        passwd = "root",
        host ="localhost",
        db = "ubion"
        )
        self.cursor = self._db.cursor(pymysql.cursors.DictCursor)

    def execute(self, input_sql, input_value = {}):
        self.cursor.execute(input_sql, input_value)

    def executeAll(self, input_sql, input_value = {}):
        self.cursor.execute(input_sql, input_value)
        self.result = self.cursor.fetchall()
        return self.result 

    def commit(self):
        self._db.commit()
        
