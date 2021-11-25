import pymysql
dbinfo = {
    'host':'10.1.10.114',
    'user':'admin',
    'password':'111111',
    'port':3306
}

class Data_Connect():
    def __init__(self,db_cof = dbinfo,dbname = None):
        '''dbname可以是元组和字典，也可以是无'''
        self.db_cof = db_cof
        self.db = pymysql.connect(database=dbname,cursorclass=pymysql.cursors.DictCursor,**db_cof)
        self.cursor = self.db.cursor()

    def select_sql(self,sql):
        self.cursor.execute(sql)
        a = self.cursor.fetchall()
        return a

    def execute_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self,sql):
        self.db.close()


if __name__ == '__main__':
    data = Data_Connect(dbname='hrspl')
    sql = "SELECT * FROM hrspl.spl_vip_task_record where uid =  1980788"
    a = data.select_sql(sql)
    print(a)


