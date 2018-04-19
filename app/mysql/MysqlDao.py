# -*- coding: UTF-8 -*-
from flask import current_app
import MySQLdb


class MysqlDao(object):
    def __init__(self):
        app = current_app._get_current_object()

        self.BetaDbHost = app.config['BETA_DB_HOST']
        self.BetaDbPort = int(app.config['BETA_DB_PORT'])
        self.BetaDbUser = app.config['BETA_DB_USER']
        self.BetaDbPasswd = app.config['BETA_DB_PASSWORD']

        self.ParseDbHost = app.config['PARSE_DB_HOST']
        self.ParseDbPort = int(app.config['PARSE_DB_PORT'])
        self.ParseDbUser = app.config['PARSE_DB_USER']
        self.ParseDbPasswd = app.config['PARSE_DB_PASSWORD']
        self.ParseDbSchema = app.config['PARSE_DB_SCHEMA']

        self.InceptionHost = app.config['INCEPTION_HOST']
        self.InceptionPort = int(app.config['INCEPTION_PORT'])

    def ConnectBetaDb(self, ResultType, Sql, LoginDb):
        status = 1
        msg = ''
        result = None

        result = self.ConnectDB(ResultType, Sql, self.BetaDbHost,
                                self.BetaDbPort, self.BetaDbUser,
                                self.BetaDbUser, self.BetaDbPasswd,
                                LoginDb)
        if result['status'] == -1:
            status = result['status']
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': result}

        return {'status': status, 'msg': msg, 'data': result['data']}

    def ConnectParseDb(self, ResultType, Sql):
        status = 1
        msg = ''
        result = None

        result = self.ConnectDB(ResultType, Sql, self.ParseDbHost,
                                self.ParseDbPort, self.ParseDbUser,
                                self.ParseDbPasswd, self.ParseDbSchema)
        if result['status'] == -1:
            status = result['status']
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': result}

        return {'status': status, 'msg': msg, 'data': result['data']}

    def ConnectInception(self, Sql):
        status = 1
        msg = ''
        result = None

        result = self.ConnectDB('all', Sql, self.InceptionHost,
                                self.InceptionPort, '', '', '')

        if result['status'] == -1:
            status = result['status']
            msg = result['msg']
            return {'status': status, 'msg': msg, 'data': result}

        return {'status': status, 'msg': msg, 'data': result['data']}

    def ConnectDB(self, ResultType, Sql, DbHost, DbPort, DbUser, DbPasswd, LoginDb):
        status = 1
        msg = ''

        conn = None
        cur = None
        result = None

        try:
            conn = MySQLdb.connect(host=DbHost,
                                   user=DbUser,
                                   passwd=DbPasswd,
                                   db=LoginDb,
                                   port=DbPort,
                                   charset='utf8mb4')
            cur = conn.cursor()
            cur.execute(Sql)
            if ResultType.lower() == 'one':
                result = cur.fetchone()
            else:
                result = cur.fetchall()

        except MySQLdb.Error as e:
            status = -1
            msg = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print msg
            return {'status': status, 'msg': msg, 'data': result}

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return {'status': status, 'msg': msg, 'data': result}
