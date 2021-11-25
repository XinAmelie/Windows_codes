from config.settings import Settings as ST
from exts.comExts.database_oper import MysqlHelp
from exts.comExts.read_yaml import read_yaml


def excute_sql(sql):
    '''执行sql'''
    dbinfo = read_yaml(ST.CASEDATA)['DBinfo']
    db = MysqlHelp(dbinfo['host'],dbinfo['user'],dbinfo['passwd'],dbinfo['database'])
    db.insert_delete_update(sql)
    return db

def select_sql(sql):
    dbinfo1 = read_yaml(ST.CASEDATA)['DBinfo']
    db = MysqlHelp(dbinfo1['host'], dbinfo1['user'], dbinfo1['passwd'], dbinfo1['database'])
    res = db.select_fetchall(sql)
    return res


if __name__ == '__main__':
    sql = "delete from hruc.uc_member where uid = 9"
    res = select_sql(sql)
    print(res)

    sql = "INSERT INTO `hruc`.`uc_member` (`uid`, `username`, `nickname`, `email`, `sanmaouid`, `studentid`, `classid`, `password`, `salt`, `lastloginip`, `lastlogintime`, `lastactivetime`, `status`, `level`, `avatarver`, `failcount`, `faillogintime`, `modular`, `classid_shared`, `mobile`, `vip`, `friends`, `app_msg`, `updatetime`, `msg_auth`) VALUES ('8', '一二三五', '一二三五', 'c838af0a951c9de46a140357b4ddfa05', '0f955358e75d446586e1335a8d44421f', '110300415', '0', '1b167f6024af4f3074e7bf42045f6919', '0b4c56', '167840318', '1629795371', '1547452612', '1', '1', '5', '0', '0', '4', '0', NULL, '0', '0', '1', '2021-08-24 16:56:12', '1,2,3,4,5,6')"
    excute_sql(sql)






