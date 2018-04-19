# -*-coding: utf-8-*-
from flask import current_app
from .MysqlDao import MysqlDao
from app.models import SchemaList, DatabaseType, DatabaseInstanceList


class Inception(object):
    def __init__(self):
        app = current_app._get_current_object()

        self.InceptionHost = app.config['INCEPTION_HOST']
        self.InceptionPort = int(app.config['INCEPTION_PORT'])
        self.MysqlHost = '192.168.199.134'
        self.MysqlPort = int('3306')
        self.MysqlUser = 'chenqi'
        self.MysqlPasswd = 'chenqi'

    def GetDBInfo(self, db_name):
        status = 1
        msg = ''
        data = []
        db_dict = {}

        db_type_id = DatabaseType.query.filter_by(name='mysql').first().id
        schema_info = SchemaList.query.filter_by(name=db_name).first()
        sub_schema_info = SchemaList.query.filter_by(parent_id=schema_info.id).all()

        if sub_schema_info:
#       判读是否是分区的库,如果是的话,需要再每个子库上执行一遍SQL
            for row in sub_schema_info:
                sub_schema_ins_id = row.instance_id
                sub_schema_ins_name = row.name
                sub_schema_arc_id = row.archive_schema_id

                sub_db_info = DatabaseInstanceList.query.filter_by(id=sub_schema_ins_id).first()
                if sub_db_info.vip:
                    db_dict = {'host': sub_db_info.vip,
                               'port': sub_db_info.port,
                               'name': sub_schema_ins_name}

                else:
                    db_dict = {'host': sub_db_info.ip,
                               'port': sub_db_info.port,
                               'name': sub_schema_ins_name}
                data.append(db_dict)

                if sub_schema_arc_id != -1:
#               如果存在归档库,语句需要在归档库也要执行一遍
                    arc_sub_schema_info = SchemaList.query.filter_by(id=sub_schema_arc_id).first()
                    arc_sub_ins_id = arc_sub_schema_info.instance_id
                    arc_sub_ins_name = arc_sub_schema_info.name

                    arc_sub_db_info = DatabaseInstanceList.query.filter_by(id=arc_sub_ins_id).first()
                    if arc_sub_db_info.vip:
                        db_dict = {'host': arc_sub_db_info.vip,
                                   'port': arc_sub_db_info.port,
                                   'name': arc_sub_ins_name}

                    else:
                        db_dict = {'host':arc_sub_db_info.ip,
                                   'port':arc_sub_db_info.port,
                                   'name':arc_sub_ins_name}
                    data.append(db_dict)

        else:
            db_info = DatabaseInstanceList.query.filter_by(id=schema_info.instance_id).first()
            if db_info.vip:
                db_dict = {'host':db_info.vip,
                           'port':db_info.port,
                           'name':db_name}
            else:
                db_dict = {'host':db_info.ip,
                           'port':db_info.port,
                           'name':db_name}
            data.append(db_dict)

            if schema_info.archive_schema_id != -1:
#               存在归档数据库的情况
                arc_schema_info = SchemaList.query.filter_by(id=schema_info.archive_schema_id).first()
                arc_ins_id = arc_schema_info.instance_id
                arc_ins_name = arc_schema_info.name

                arc_db_info = DatabaseInstanceList.query.filter_by(id=arc_ins_id).first()
                if arc_db_info.vip:
                    db_dict = {'host': arc_db_info.vip,
                               'port': arc_db_info.port,
                               'name': arc_ins_name}

                else:
                    db_dict = {'host':arc_db_info.ip,
                               'port':arc_db_info.port,
                               'name':arc_ins_name}
                data.append(db_dict)

        return {'status': status, 'msg': msg, 'data': data}
        
    def InceptionReview(self, DbName, SqlText):
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()

        InceptionSql = "/*--host=%s;\
                          --port=%s;\
                          --user=%s;\
                          --password=%s;\
                          --enable-check=1;*/\
                       inception_magic_start;\
                       use %s;\
                       %s\
                       inception_magic_commit;" \
                       % (self.MysqlHost, self.MysqlPort, self.MysqlUser,
                          self.MysqlPasswd, DbName, SqlText)
        InceptionResult = mysqldao.ConnectInception(InceptionSql)

        status = InceptionResult['status']
        msg = InceptionResult['msg']
        if status == -1:
            return {'status': status, 'msg': msg, 'data': data}

        for row in InceptionResult['data']:
            if row[0] == 1:
                pass
            else:
                if row[4] == 'None':
                    data.append('')
                else:
                    data.append(row[4])
        return {'status': status, 'msg': msg, 'data': data}

    def InceptionSplit(self, db_host, db_port, db_name, sql_text):
#       Inception执行SQL之前,预处理语句
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()

        inception_split_sql = "/*--host=%s;\
                                --port=%s;\
                                --user=%s;\
                                --password=%s;\
                                --enable-ignore-warnings;\
                                --enable-split;*/\
                                inception_magic_start;\
                                use %s;\
                                %s\
                                inception_magic_commit;" \
                                % (db_host, db_port, self.MysqlUser,
                                    self.MysqlPasswd, db_name, sql_text)
        split_result = mysqldao.ConnectInception(inception_split_sql)
        status = split_result['status']
        msg = split_result['msg']
        if status == -1:
            return {'status': status, 'msg': msg, 'data': data}

        data = split_result['data']
        return {'status': status, 'msg': msg, 'data': data}

    def InceptionExecuteDDL(self, db_name, sql_text):
#       将sql交给inception进行最终执行，并返回执行结果。
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()
        dbinfo_result = self.GetDBInfo(db_name)
        if dbinfo_result['status'] == -1:
            status = dbinfo_result['status']
            msg = dbinfo_result['msg']
            return {'status': status, 'msg': msg, 'data': data}

        for dbinfo in dbinfo_result['data']:
            db_name = dbinfo['name']
            db_host = dbinfo['host']
            db_port = dbinfo['port']

            split_result = self.InceptionSplit(db_host, db_port, db_name, sql_text)
            status = split_result['status']
            msg = split_result['msg']
            if status == -1:
                return {'status': status, 'msg': msg, 'data': data}

            for split_sql in split_result['data']:
                inception_exec_sql = "/*--host=%s;\
                                     --port=%s;\
                                     --user=%s;\
                                     --password=%s;\
                                     --enable-ignore-warnings;\
                                     --disable-remote-backup;\
                                     --enable-execute;*/\
                                     inception_magic_start;\
                                     %s\
                                     inception_magic_commit;" \
                                     % (db_host, db_port,
                                        self.MysqlUser, self.MysqlPasswd,
                                        split_sql[1])
                result = mysqldao.ConnectInception(inception_exec_sql)

                if result['status'] == -1:
                    status = result['status']
                    msg = result['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                for row in result['data']:
                    if row[4] != 'None':
                        status = -1
                        msg += row[4]
                        return {'status': status, 'msg': msg, 'data': data}

        return {'status': status, 'msg': msg, 'data': data}

    def InceptionExecuteDML(self, db_name, sql_text, if_need_backup):
        """
        将sql交给inception进行最终执行，并返回执行结果。
        """
        status = 1
        msg = ''
        data = []

        mysqldao = MysqlDao()
        schema_info = SchemaList.query.filter_by(name=db_name).first()
        schema_instance_id = schema_info.instance_id
        db_info = DatabaseInstanceList.query.filter_by(id=schema_instance_id).first()

        if db_info.vip:
            db_host = db_info.vip
        else:
            db_host = db_info.host
        db_port = db_info.port

        if if_need_backup == "1":
            backup_key_word = "--enable-remote-backup;"
        else:
            backup_key_word = "--disable-remote-backup;"

        split_result = self.InceptionSplit(db_host, db_port, db_name, sql_text)
        status = split_result['status']
        msg = split_result['msg']
        if status == -1:
            return {'status': status, 'msg': msg, 'data': data}

        for split_sql in split_result['data']:
            inception_exec_sql = "/*--host=%s;\
                                  --port=%s;\
                                  --user=%s;\
                                  --password=%s;\
                                  --enable-ignore-warnings;\
                                  %s\
                                  --enable-execute;*/\
                                  inception_magic_start;\
                                  use %s;\
                                  %s\
                                  inception_magic_commit;" \
                                  % (db_host, db_port,
                                     self.MysqlUser, self.MysqlPasswd,
                                     backup_key_word, db_name, split_sql[1])
            result = mysqldao.ConnectInception(inception_exec_sql)

            status = result['status']
            msg = result['msg']
            if status == -1:
                return {'status': status, 'msg': msg, 'data': data}
            data.append(result['data'])

        return {'status': status, 'msg': msg, 'data': data} 