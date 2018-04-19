# -*-coding: utf-8-*-
from flask import current_app
from .MysqlParse import MysqlParse
from .SqlRulesDIY import CheckDDLSql, CheckDMLSql
from .Inception import Inception
from app.redis.RedisDao import RedisDao


class SqlReview(object):
    def __init__(self):
        pass

    def SqlReview(self, db_name, sql_text, sql_type):
        status = 1
        msg = ''
        data = []
        check_result = ''
        mysqlparse = MysqlParse()
        checkddlsql = CheckDDLSql()
        checkdmlsql = CheckDMLSql()
        inception = Inception()
        redisdao = RedisDao()

        result = mysqlparse.SplitSql(db_name, sql_text)
#       首先对语句块进行切分
        status = result['status']
        if status != 1:
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': data}
        split_sql = result['data']

        for sql in split_sql:
            result = mysqlparse.GetSqlInfo(db_name, sql)
#           获得语句的类型
            if result['status'] != 1:
                status = result['status']
                msg = result['msg']
                return {'status': status, 'msg': msg, 'data': data}
            sql_info = result['data']

            if sql_type.lower() == 'dml':
                if sql_info['type'] not in ('update', 'delete', 'insert'):
                    status = -1
                    msg = '内容中包含表结构定义语句,请分开提交.'
                    return {'status': status, 'msg': msg, 'data': data}

                else:
                    result = checkdmlsql.CheckSql(sql)
#                   进行SQL自定义规则校验
                    status = result['status']
                    if status == -1:
                        msg = result['msg']
                        return {'status': status, 'msg': msg, 'data': data}
                    for row in result['data']:
                        check_result += row

#                   进行Inception校验
                    result = inception.InceptionReview(db_name, sql)
                    status = result['status']
                    if status == -1:
                        msg = result['msg']
                        return {'status': status, 'msg': msg, 'data': data}
                    check_result += result['data'][0]
                    data.append({'sql': sql, 'result': check_result})

            elif sql_type.lower() == 'ddl':
                if sql_info['type'] not in ('create', 'modify'):
                    status = -1
                    msg = '内容中包含数据变更语句,请分开提交.'
                    return {'status': status, 'msg': msg, 'data': data}

                elif sql_info['type'] == 'modify':
                    result = mysqlparse.AlterToCreate(db_name, sql_info['name'], sql)
                    status = result['status']
                    if status != 1:
                        msg = result['msg']
                        return {'status': status, 'msg': msg, 'data': data}
                    new_sql = result['data']
                elif sql_info['type'] == 'create':
                    new_sql = sql

#               进行SQL自定义规则校验
                result = checkddlsql.CheckSql(db_name, sql_info['name'], new_sql)
                status = result['status']
                if status == -1:
                    msg = result['msg']
                    return {'status': status, 'msg': msg, 'data': data}
                for row in result['data']:
                    check_result += row

#               进行Inception校验
                result = inception.InceptionReview(db_name, new_sql)
                status = result['status']
                if status == -1:
                    msg = result['msg']
                    return {'status': status, 'msg': msg, 'data': data}
                check_result += result['data'][0]

#               清理Redis
                """
                if check_result == '':
                    redisdao.RedisRename(db_name + '|' + sql_info['name'] + '|tmp',
                                         db_name + '|' + sql_info['name'])
                else:
                    redisdao.RedisDel(db_name + '|' + sql_info['name'] + '|tmp')
                """

                data.append({'sql': sql, 'result': check_result})

        return {'status': status, 'msg': msg, 'data': data}
