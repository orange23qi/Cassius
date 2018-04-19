# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    group_id = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ProjectTeam(db.Model):
    __tablename__ = 'config_project_teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class DBATeam(db.Model):
    __tablename__ = 'config_dba_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class SchemaList(db.Model):
    __tablename__ = 'schema_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    instance_id = db.Column(db.Integer, index=True)
    type = db.Column(db.SmallInteger)
    parent_id = db.Column(db.Integer, default=-1, index=True)
    project_team_id = db.Column(db.Integer, index=True)
    is_sharding = db.Column(db.SmallInteger, default=-1)
    is_archive = db.Column(db.SmallInteger, default=-1)
    archive_schema_id = db.Column(db.Integer, default=-1)
    create_time = db.Column(db.DateTime, index=True)
    update_time = db.Column(db.DateTime, index=True)


class SchemaType(db.Model):
    __tablename__ = 'config_schema_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class DatabaseInstanceList(db.Model):
    __tablename__ = 'database_instance_list'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    vip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    type = db.Column(db.SmallInteger)
    db_area_id = db.Column(db.SmallInteger)
    parent_id = db.Column(db.Integer, default=-1, index=True)
    create_time = db.Column(db.DateTime, index=True)
    update_time = db.Column(db.DateTime, index=True)


class DatabaseType(db.Model):
    __tablename__ = 'config_database_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class DatabaseArea(db.Model):
    __tablename__ = 'config_db_area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class OrderList(db.Model):
    __tablename__ = 'order_list'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    order_title = db.Column(db.String(64))
    order_type = db.Column(db.Integer)
    db_type = db.Column(db.Integer)
    order_status = db.Column(db.SmallInteger)
    auditor_id = db.Column(db.Integer, index=True)
    current_user_id = db.Column(db.Integer, index=True)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, onupdate=datetime.now, default=datetime.now)


class OrderType(db.Model):
    __tablename__ = 'config_order_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class OrderStatus(db.Model):
    __tablename__ = 'config_order_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class OrderMysqlDDLInfo(db.Model):
    __tablename__ = 'order_mysql_ddl_info'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, index=True)
    order_title = db.Column(db.String(64))
    db_name = db.Column(db.String(64))
    remark_text = db.Column(db.Text)
    sql_text = db.Column(db.Text)
    auditor_id = db.Column(db.Integer, index=True)
    current_user_id = db.Column(db.Integer, index=True)
    order_status = db.Column(db.SmallInteger, default=0)
    dba_suggest = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, onupdate=datetime.now, default=datetime.now)

class OrderMysqlDMLInfo(db.Model):
    __tablename__ = 'order_mysql_dml_info'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, index=True)
    order_title = db.Column(db.String(64))
    db_name = db.Column(db.String(64))
    remark_text = db.Column(db.Text)
    sql_text = db.Column(db.Text)
    is_backup = db.Column(db.SmallInteger)
    auditor_id = db.Column(db.Integer, index=True)
    current_user_id = db.Column(db.Integer, index=True)
    order_status = db.Column(db.SmallInteger, default=0)
    dba_suggest = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, onupdate=datetime.now, default=datetime.now)

class OrderMysqlCreateDbInfo(db.Model):
    __tablename__ = 'order_mysql_createdb_info'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, index=True)
    project_team_id = db.Column(db.Integer, index=True)
    project_remark = db.Column(db.Text)
    db_name = db.Column(db.String(64))
    prediction = db.Column(db.Text)
    db_area_id = db.Column(db.SmallInteger)
    info_status = db.Column(db.SmallInteger, default=0)
    complete_time = db.Column(db.DateTime)
    auditor_id = db.Column(db.Integer, index=True)
    reviewer_remark = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True, onupdate=datetime.now, default=datetime.now)
