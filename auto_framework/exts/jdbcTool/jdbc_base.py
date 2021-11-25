import os
import jaydebeapi

from core.utils import read_yaml
from config.settings import Settings as ST


tools_path = os.path.join(ST.EXTS_PATH,'jdbcTool')


class JdbcBase(object):
    '''通过jdbc方式连接各种数据库'''

    def __init__(self,url,jarName,driverClass,user,psw):
        self.user = user
        self.passwd = psw
        self.url = url
        self.driver = driverClass
        self.jarFile = os.path.join(tools_path,'jarFile',jarName)

    def open_coon(self):
        '''创建连接'''
        self.conn = jaydebeapi.connect(self.driver, self.url, [self.user, self.passwd], self.jarFile)
        self.curs = self.conn.cursor()

    def close(self):
        '''关闭连接'''
        self.curs.close()
        self.conn.close()

    def insert_delete_update(self,sql):
        '''调用执行语句：增、删、改'''
        try:
            self.open_coon()
            self.curs.execute(sql)
            self.conn.commit()
            self.close()
        except Exception as erorr:
            print(erorr)

    def select_fetchall(self,sql):
        '''调用查询语句'''
        try:
            self.open_coon()
            self.curs.execute(sql)
            results = self.curs.fetchall()
            self.close()
            return results
        except Exception as erorr:
            print(erorr)


class SqliteDB():

    def __init__(self,path,user,psw):
        url,jarName,driverClass = self.get_dbInfo(path)
        self.jdbc = JdbcBase(url,jarName,driverClass,user,psw)

    def get_dbInfo(self,path):
        '''获取数据库信息'''
        sqlite_data = read_yaml(ST.DATABASEINFO)['sqlite']
        url = sqlite_data['url模板'].replace('{dbPATH}',path)
        jarName = sqlite_data['添加文件']
        driverClass = sqlite_data['类名']
        return url,jarName,driverClass

    def sqlite_select(self,sql):
        '''sqlite数据库查询'''
        return self.jdbc.select_fetchall(sql)

    def sqlite_commit(self,sql):
        '''sqlite数据库增删改'''
        return self.jdbc.insert_delete_update(sql)


if __name__ == '__main__':
    url = 'jdbc:mysql://127.0.0.1:3306/lportal?serverTimezone=Asia/Shanghai&useSSL=false'
    user = 'root'
    psw = '1111'
    jarName = 'mysql-connector-java-8.0.17.jar'
    sql = 'select * from journalarticle;'
    driverClass = 'com.mysql.cj.jdbc.Driver'
    jdbc = JdbcBase(url,jarName,driverClass,user,psw)
    res = jdbc.select_fetchall(sql)
    print(res)