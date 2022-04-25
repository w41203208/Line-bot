import pymysql

# test
# DB_CONFIG = {
# 	"host": "127.0.0.1",
# 	"port": 3306,
# 	"user": "root",
# 	"passwd": "0000",
# 	"db": "temp_database2",
#   "charset": "utf8",
# }


# formal
DB_CONFIG = {
	"host": "127.0.0.1",
	"port": 3306,
	"user": "root",
	"passwd": "kcsau4a83",
	"db": "kcs_backend",
  "charset": "utf8",
}

class SQLManger(object):
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    self.conn = None
    self.cursor = None

  def connect(self):
    self.conn = pymysql.connect(
			host=DB_CONFIG["host"],
			port=DB_CONFIG["port"],
			user=DB_CONFIG["user"],
			passwd=DB_CONFIG["passwd"],
			db=DB_CONFIG["db"],
			charset=DB_CONFIG["charset"]
		)
    self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

  def query(self, sql , args=None):
    self.cursor.execute(sql, args)
    result = self.cursor.fetchall()
    return result

  def update(self, sql, args=None):
    self.cursor.execute(sql, args)
    self.conn.commit()

  def close(self):
    self.cursor.close()
    self.conn.close()

