import pymysql
from utils.log import log


class ConnectMysql(object):
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, user, password, port, database):
        if self.init_flag:
            return
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.cursor = self.db.cursor()
            log.debug(f"mysql connect success!")
        except Exception as msg:
            self.cursor = None
            log.error(f"mysql connect error: {msg}")
        self.init_flag = True

    def query_sql(self, sql):
        """查询，返回结果"""
        if self.cursor:
            log.debug(f"query sql: {sql}!")
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                if len(result) == 1:
                    result = result[0]
                elif len(result) == 0:
                    result = None
                log.info(f"query result: {result}")
                return result
            except Exception as msg:
                log.error(f"query error: {msg}")

    def execute_sql(self, sql):
        """修改，新增，删除"""
        if self.cursor:
            log.debug(f"execute sql: {sql}")
            try:
                result = self.cursor.execute(sql)
                print(result)
                log.debug(f"execute result: {result}")
                self.db.commit()
            except Exception as msg:
                log.error(f"execute error: {msg}")

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.db.close()
            log.debug(f"close db!")
