# -*-coding: utf-8-*-
# yamlfile example:
# http://gitlab.1dmy.com/ezbuy/garencieres/blob/master/service/internal/redis-orm/tag.yaml

from flask import current_app
import random
import string
import os
from .MysqlDao import MysqlDao
from .MysqlParse import MysqlParse
from .AnalyzeYaml import AnalyzeYaml


class YamlToSql(object):
    def __init__(self):
        pass

    def YamlToAlter(self, DbName, SqlText):
        """
        yaml文件转成Alter语句
        """
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()
        analyzeyaml = AnalyzeYaml()

#       转换成Create语句
        result = analyzeyaml.YamlToCreate(SqlText)
        status = result['status']
        msg = result['msg']
        if status == -1:
            return {'status': status, 'msg': msg, 'data': data}

        for TableInfo in result['data']:
            TableName = TableInfo['name']
            SqlText = TableInfo['sql']

#           到目标库中查一下该表是否已经存在
            result = self.CheckTableIfExists(DbName, TableName)
            status = result['status']
            msg = result['msg']
            if status == -1:
                return {'status': status, 'msg': msg, 'data': data}

            if result['data'][0] == 1:
                """
                生成随机新表名,然后在建一张临时表
                """
                Str = ''.join(random.sample(string.ascii_letters + string.digits, 12))
                NewTableName = 'tmp_' + Str.lower()
                TmpDbName = DbName.lower() + '.'
                SqlText = SqlText.replace('`', '').lower().replace(TmpDbName, '')
                SqlText = SqlText.replace(TableName.lower(), NewTableName)

                CreateResult = mysqldao.ConnectParseDb('one', SqlText)
                status = CreateResult['status']
                msg = CreateResult['msg']
                if status != 1:
                    return {'status': status, 'msg': msg, 'data': data}

                DiffResult = self.ExMysqlDiff(DbName, TableName, NewTableName)
                status = DiffResult['status']
                msg = DiffResult['msg']
                if status == -1:
                    return {'status': status, 'msg': msg, 'data': data}

                data.append(DiffResult['data'][0].replace(NewTableName, TableName))

#               回收临时表
                SqlDropTempTable = "DROP TABLE %s;" % NewTableName
                result = self.ConnectParseDb('one', SqlDropTempTable)
                status = result['status']
                msg = result['msg']
                if status != 1:
                    return {'status': status, 'msg': msg, 'data': data}
            else:
                data.append(SqlText)

        return {'status': status, 'msg': msg, 'data': data}

    def CheckTableIfExists(self, DbName, TableName):
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()

        SqlIfExists = "select count(1) from \
                      information_schema.tables \
                      where table_schema = '%s' \
                      and table_name = '%s';" % (DbName, TableName)
        result = mysqldao.ConnectParseDb('one', SqlIfExists)

        status = result['status']
        msg = result['msg']
        if status == -1:
            return {'status': status, 'msg': msg, 'data': data}

        data = result['data']
        return {'status': status, 'msg': msg, 'data': data}

    def ExMysqlDiff(self, DbName, TableName, NewTableName):
        status = 1
        msg = ''
        data = []

        mysqlDiffCommand = "mysqldiff --server1=%s:%s@%s:%s --server2=%s:%s@%s:%s \
                            %s.%s:%s.%s -d sql|egrep -v '^#|^$'" \
                            % (self.ParseDbUser, self.ParseDbPasswd,
                               self.ParseDbHost, self.ParseDbPort,
                               self.BetaDbUser, self.BetaDbPasswd,
                               self.BetaDbHost, self.BetaDbPort,
                               self.ParseDbSchema, NewTableName, DbName,
                               TableName)
        print mysqlDiffCommand
        diffResult = os.popen(mysqlDiffCommand)
        Sql = diffResult.read()
        Sql = Sql.replace('`', '').replace(self.ParseDbSchema+'.', '')
        Sql = Sql.replace('Compare failed. One or more differences found.', '')
        if isinstance(Sql, unicode):
            data.append(Sql)
        else:
            data.append(Sql.decode('utf-8'))

        return {'status': status, 'msg': msg, 'data': data}
