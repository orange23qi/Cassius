# -*- coding: utf-8 -*-
from flask import current_app
import random
import string
import sqlparse
from .MysqlDao import MysqlDao
from app.redis.RedisDao import RedisDao


class MysqlParse(object):
    def __init__(self):
        app = current_app._get_current_object()

        self.ParseDbHost = app.config['PARSE_DB_HOST']
        self.ParseDbPort = int(app.config['PARSE_DB_PORT'])
        self.ParseDbUser = app.config['PARSE_DB_USER']
        self.ParseDbPasswd = app.config['PARSE_DB_PASSWORD']
        self.ParseDbSchema = app.config['PARSE_DB_SCHEMA']

    def SplitSql(self, db_name, sql):
        """
        将一整坨的sql语句拆分开来
        """
        status = 1
        msg = ''
        data = []

        parsed = sqlparse.parse(sql.replace('\n\n', ''))
        for rows in parsed:
            value = ''
            value = rows.value.lstrip()
            if value is not None and value != '':
                data.append(value)

        return {'status': status, 'msg': msg, 'data': data}

    def GetSqlInfo(self, db_name, sql):
#       解析ddl语句,取得语句类型/以及表名
        status = 1
        msg = ''
        data = None
        tb_name = ''
        sql_type = ''
#       初始化sql
        sql = sql.replace('(', ' ').lower()
        sql = sql.replace('\r', '').replace('\n', '').replace('\t', '')
#       去除多余空格
        sql = ' '.join(sql.split())
#       去除关键字
        key_word_list = ['`', db_name+'.', 'if not exists', 'temporary',
                         'unique', 'fulltext', 'spatial', 'using btree',
                         'using hash']
        for key_word in key_word_list:
            sql = sql.replace(key_word, '')

        sql_split = sql.split()

        if sql_split[0] == 'create':
            if sql_split[1] == 'table':
                sql_type = 'create'
                tb_name = sql_split[2]
            elif sql_split[1] == 'index':
                sql_type = 'modify'
                tb_name = sql_split[4]
            else:
                status = -1
                if len(sql_split) == 1:
                    msg = u'不支持的Sql类型(%s)' % (sql_split[0])
                else:
                    msg = u'不支持的Sql类型(%s %s)' % (sql_split[0], sql_split[1])

        elif sql_split[0] == 'alter' and sql_split[1] == 'table':
            sql_type = 'modify'
            tb_name = sql_split[2]
        elif sql_split[0] in ('update', 'delete', 'insert'):
            sql_type = sql_split[0]
            tb_name = ''
        else:
            status = -1
            if len(sql_split) == 1:
                msg = u'不支持的Sql类型(%s)' % (sql_split[0])
            else:
                msg = u'不支持的Sql类型(%s %s)' % (sql_split[0], sql_split[1])

        data = {'name': tb_name, 'type': sql_type}
        return {'status': status, 'msg': msg, 'data': data}

    def GetTableDict(self, db_name, tb_name, sql_text):
        """
        根据建表语句返回表结构的数据字典
        """
        status = 1
        msg = ''
        data = []
        ColInfo = []
        mysqldao = MysqlDao()

#       生成临时表
        result = self.CreateTempTable(db_name, tb_name, sql_text)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        new_tb_name = result['data']

#       开始解析表结构
        SqlGetColInfo = "SELECT column_name, \
                                data_type, \
                                character_maximum_length, \
                                is_nullable \
                        FROM information_schema.columns \
                        WHERE table_schema = '%s' \
                        AND table_name = '%s';"\
                        % (self.ParseDbSchema, new_tb_name)
        result = mysqldao.ConnectParseDb('all', SqlGetColInfo)
        status = result['status']
        msg = result['msg']
        if status != 1:
            return {'status': status, 'msg': msg, 'data': data}

        for ColDetail in result['data']:
            ColName = ColDetail[0]
            ColType = ColDetail[1]
            ColLen = ColDetail[2]
            if ColDetail[3].lower() == 'no':
                ColIsNull = 0
            else:
                ColIsNull = 1

            SqlGetIdxInfo = "SELECT count(1) \
                            FROM information_schema.statistics \
                            WHERE table_schema = '%s' \
                            AND table_name = '%s' \
                            AND column_name = '%s';"\
                            % (self.ParseDbSchema, new_tb_name, ColName)
            result = mysqldao.ConnectParseDb('one', SqlGetIdxInfo)
            status = result['status']
            msg = result['msg']
            if status != 1:
                return {'status': status, 'msg': msg, 'data': data}

            if result['data'] > 0:
                ColIsKey = 1
            else:
                ColIsKey = 0

            ColInfo.append({'name': ColName,
                            'type': ColType,
                            'len': ColLen,
                            'isnull': ColIsNull,
                            'iskey': ColIsKey})

        SqlGetTableEngine = "SELECT engine \
                            FROM information_schema.tables \
                            WHERE table_name = '%s' \
                            AND table_schema = '%s';" \
                            % (new_tb_name, self.ParseDbSchema)
        result = mysqldao.ConnectParseDb('one', SqlGetTableEngine)
        status = result['status']
        msg = result['msg']
        if status != 1:
            return {'status': status, 'msg': msg, 'data': data}

        TableEngine = result['data'][0].lower()

        TableInfo = {'name': tb_name,
                     'engine': TableEngine,
                     'columns': ColInfo}
        data.append(TableInfo)
#       回收临时表
        result = self.DropTempTable(new_tb_name)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}

        return {'status': status, 'msg': msg, 'data': data}

    def CreateTempTable(self, db_name, tb_name, sql_text):
        """
        根据语句生成临时表,并返回临时表名
        """
        status = 1
        msg = ''
        data = None
        mysqldao = MysqlDao()
        redisdao = RedisDao()

#       生成随机新表名
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 12))
        new_tb_name = 'tmp_' + random_str.lower()
        new_db_name = db_name.lower() + '.'

        if isinstance(sql_text, unicode) is False:
            sql_text = sql_text.decode("utf-8")
        sql_text = sql_text.replace('`', '').lower().replace(new_db_name, '')
        sql_text = sql_text.replace('\r', '').replace('\n', '').replace('\t', '')

        new_sql_text = sql_text.replace(tb_name.lower(), new_tb_name)

#       执行,生成临时表
        result = mysqldao.ConnectParseDb('one', new_sql_text)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        data = new_tb_name

#       将表结构存入redis
        result = redisdao.RedisSet(db_name + '|' + tb_name, sql_text)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}

        return {'status': status, 'msg': msg, 'data': data}

    def DropTempTable(self, tb_name):
        """
        根据表名,回收临时表
        """
        status = 1
        msg = ''
        data = None
        mysqldao = MysqlDao()

#       回收临时表
        sql_drop_temp_table = "DROP TABLE %s;" % tb_name
        result = mysqldao.ConnectParseDb('one', sql_drop_temp_table)
        msg = result['msg']
        if status != 1:
            status = result['status']
            return {'status': status, 'msg': msg, 'data': data}

        return {'status': status, 'msg': msg, 'data': data}

    def AlterToCreate(self, db_name, tb_name, sql_text):
#       根据modify语句,获取包含create + alter内容的新Create语句
        status = 1
        msg = ''
        data = None
        redisdao = RedisDao()
        mysqldao = MysqlDao()

        result = redisdao.RedisGet(db_name + '|' + tb_name)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        redis_result = result['data']

        if redis_result is None:
#           如果redis里边没有对应的key,就到源库里边去捞
            sql = "SHOW CREATE TABLE %s;" % tb_name
            result = mysqldao.ConnectBetaDb('one', sql, db_name)
            status = result['status']
            if status != 1:
                msg = result['msg']
                return {'status': status, 'msg': msg, 'data': data}
            redis_result = result['data'][1] + ';'

#       创建临时表
        result = self.CreateTempTable(db_name, tb_name, redis_result)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        new_tb_name = result['data']

#       应用modify语句
        new_db_name = db_name.lower() + '.'
        sql_text = sql_text.replace('`', '').lower().replace(new_db_name, '')
        sql_text = sql_text.replace('\r', '').replace('\n', '').replace('\t', '')
        if isinstance(sql_text, unicode) is False:
            sql_text = sql_text.decode("utf-8")

        new_sql_text = sql_text.replace(tb_name.lower(), new_tb_name)
        result = mysqldao.ConnectParseDb('one', new_sql_text)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}

#       获取新的表结构
        sql = "SHOW CREATE TABLE %s;" % new_tb_name
        result = mysqldao.ConnectParseDb('one', sql)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        data = result['data'][1].replace('`', '') + ';'
        data = data.replace('\r', '').replace('\n', '').replace('\t', '')
        data = data.replace(new_tb_name, tb_name.lower())

#       将表结构存入redis
#        result = redisdao.RedisSet(db_name + '|' + tb_name + '|tmp', data)
        result = redisdao.RedisSet(db_name + '|' + tb_name, data)
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}

        return {'status': status, 'msg': msg, 'data': data}