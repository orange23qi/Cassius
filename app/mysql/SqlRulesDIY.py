# -*-coding: utf-8-*-
from flask import current_app
import re

from .MysqlParse import MysqlParse


class CheckPublic(object):
    """
    返回结果值说明:
    1  : 校验通过
    2  : 校验失败
    1 : 出现语法或等等不可预知的错误
    """
    def __init__(self):
        self.KeyWordDrop = True

    def CheckIfExistsDbName(self, SqlText, DbName):
        status = 1
        msg = ''
        data = []

        if SqlText.lower().replace(DbName.lower(), '') != SqlText.lower():
            status = 2
            data.append(u'语句中不能带DbName.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckKeyWordDrop(self, SqlText):
        status = 1
        msg = ''
        data = []

        if re.match(r"([\s\S]*)drop(\s+.*)", SqlText.lower()):
            status = 2
            data.append(u'语句中不能包含DROP关键字.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckSql(self, SqlText):
        status = 1
        msg = ''
        data = []

        result = self.CheckKeyWordDrop(SqlText)
        if result['status'] == 2:
            status = result['status']
            for DataInfo in result['data']:
                data.append(DataInfo)

        if self.KeyWordDrop is True:
            result = self.CheckKeyWordDrop(SqlText)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        return {'status': status, 'msg': msg, 'data': data}


class CheckDDLSql(object):
    """
    校验内容:
    1. 语句中不能带IF NOT EXISTS
    2. "dic_"开头的表不校验存储引擎,其他表强制innodb
    3. "_date"或"mount"或"fee"或"price"结尾的字段必须是bigint类型
    4. 禁用blob/clob/text类型
    5. varchar长度不能超过1000
    6. 索引字段必须带not null属性
    7. 语句中不能带DBNAME
    8. 语句中不能包含DROP关键字
    """
    def __init__(self):
        self.KeyWordIfNotExists = True
        self.TableEngine = True
        self.ColumnDate = True
        self.ColumnMount = True
        self.ColumnFee = True
        self.ColumnPrice = True
        self.ColumnTypeBlob = True
        self.ColumnTypeClob = True
        self.ColumnTypeText = True
        self.ColumnLenVarchar = True
        self.ColumnIsIndex = True

    def CheckKeyWordIfNotExists(self, SqlText):
        status = 1
        msg = ''
        data = []

        if re.match(r"([\s\S]*)if(\s+)not(\s+)exists(\s+.*)", SqlText.lower()):
            status = 2
            data.append(u'语句中不能包含IF NOT EXISTS关键字.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckTableEngine(self, TableDict):
        status = 1
        msg = ''
        data = []

        if TableDict['engine'] != 'innodb':
            if TableDict['name'][0: 4] != 'dic_':
                status = 2
                data.append(u'不推荐'+TableDict['engine']+u',请将存储引擎改成innodb.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnDate(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['name'][-4:] == 'date':
                if ColumnInfo['type'] != 'bigint':
                    if ColumnInfo['name'][0: 1] != 'is':
                        status = 2
                        data.append(u'需要将'+ColumnInfo['name']+u'字段的类型改成bigint.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnMount(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['name'][-5:] == 'mount':
                if ColumnInfo['type'] != 'bigint':
                    if ColumnInfo['name'][0: 1] != 'is':
                        status = 2
                        data.append(u'需要将'+ColumnInfo['name']+u'字段的类型改成bigint.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnPrice(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['name'][-5:] == 'price':
                if ColumnInfo['type'] != 'bigint':
                    if ColumnInfo['name'][0: 1] != 'is':
                        status = 2
                        data.append(u'需要将'+ColumnInfo['name']+u'字段的类型改成bigint.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnFee(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['name'][-3:] == 'fee':
                if ColumnInfo['type'] != 'bigint':
                    if ColumnInfo['name'][0: 1] != 'is':
                        status = 2
                        data.append(u'需要将'+ColumnInfo['name']+u'字段的类型改成bigint.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnTypeBlob(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['type'] == 'blob':
                status = 2
                data.append(u'禁用blob类型,请将'+ColumnInfo['name']+u'修改成其他类型.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnTypeClob(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['type'] == 'clob':
                status = 2
                data.append(u'禁用clob类型,请将'+ColumnInfo['name']+u'修改成其他类型.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnTypeText(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['type'] == 'text':
                status = 2
                data.append(u'禁用text类型,请将'+ColumnInfo['name']+u'修改成其他类型.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnLenVarchar(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['type'] == 'varchar':
                if ColumnInfo['len'] > 1000:
                    status = 2
                    data.append(u'varchar类型字段'+ColumnInfo['name']+u'长度不能超过1000.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckColumnIsIndex(self, TableDict):
        status = 1
        msg = ''
        data = []

        for ColumnInfo in TableDict['columns']:
            if ColumnInfo['isnull'] == 1 and ColumnInfo['iskey'] == 1:
                status = 2
                data.append(u'索引字段'+ColumnInfo['name']+u'必须非空.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckSql(self, DbName, TableName, SqlText):
        status = 1
        msg = ''
        data = []

        checkpublic = CheckPublic()
        mysqlparse = MysqlParse()
        result = mysqlparse.GetTableDict(DbName, TableName, SqlText)
        if result['status'] != 1:
            status = result['status']
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        TableDict = result['data'][0]

        checkpublic = CheckPublic()
        result = checkpublic.CheckSql(SqlText.lower())
        if result['status'] == 2:
            status = result['status']
            for DataInfo in result['data']:
                data.append(DataInfo)

        if self.KeyWordIfNotExists is True:
            result = self.CheckKeyWordIfNotExists(SqlText)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.TableEngine is True:
            result = self.CheckTableEngine(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnDate is True:
            result = self.CheckColumnDate(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnMount is True:
            result = self.CheckColumnMount(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnPrice is True:
            result = self.CheckColumnPrice(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnFee is True:
            result = self.CheckColumnFee(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnTypeBlob is True:
            result = self.CheckColumnTypeBlob(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnTypeClob is True:
            result = self.CheckColumnTypeClob(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnTypeText is True:
            result = self.CheckColumnTypeText(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnLenVarchar is True:
            result = self.CheckColumnLenVarchar(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        if self.ColumnIsIndex is True:
            result = self.CheckColumnIsIndex(TableDict)
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)

        datastr = ''
        for row in data:
            datastr = row + '\n'
        print datastr
        return {'status': status, 'msg': msg, 'data': datastr}


class CheckDMLSql(object):
    """
    校验内容:
    1. 语句中不能包含DROP关键字
    2. 语句中不能包含TRUNCATE关键字
    3. 语句中不能带DBNAME
    """
    def __init__(self):
        self.KeyWordTruncate = True

    def CheckKeyWordTruncate(self, SqlText):
        status = 1
        msg = ''
        data = []

        if re.match(r"([\s\S]*)drop(\s+.*)", SqlText.lower()):
            status = 2
            data.append(u'语句中不能包含TRUNCATE关键字.')

        return {'status': status, 'msg': msg, 'data': data}

    def CheckSql(self, SqlText):
        status = 1
        msg = ''
        data = []

        checkpublic = CheckPublic()
        result = checkpublic.CheckSql(SqlText.lower())
        if result['status'] == 2:
            status = result['status']
            for DataInfo in result['data']:
                data.append(DataInfo)
        """
        if self.KeyWordDrop is True:
            result = self.CheckKeyWordTruncate(SqlText.lower())
            if result['status'] == 2:
                status = result['status']
                for DataInfo in result['data']:
                    data.append(DataInfo)
        """

        return {'status': status, 'msg': msg, 'data': data}
