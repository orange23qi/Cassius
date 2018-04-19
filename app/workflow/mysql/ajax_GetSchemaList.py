# -*-coding: utf-8-*-
from flask import jsonify, request, session
from . import workflow_mysql
from app.models import SchemaList


@workflow_mysql.route('/schemalist/<sql_type>', methods=['GET', 'POST'])
def MysqlSchemaList(sql_type):
    """
    获取数据库列表
    """
    data = []

    if sql_type == 'ddl':
        schemas = SchemaList.query.filter(SchemaList.parent_id == -1)
        schemas = schemas.filter(SchemaList.is_archive == -1).all()

    elif sql_type == 'dml':
        schemas = SchemaList.query.filter(SchemaList.is_sharding == -1)
        schemas = schemas.filter(SchemaList.is_archive == -1).all()

    for row in schemas:
        data.append(row.name)

    return jsonify(data=data)
