# -*-coding: utf-8-*-
from flask import jsonify, request, session
from . import workflow_mysql
from app.mysql.SqlReview import SqlReview
from app.models import SchemaList


@workflow_mysql.route('/autoreview/<checktype>', methods=['GET', 'POST'])
def AutoReview(checktype):
    """
    数据库语句校验
    """
    status = 1
    msg = ""
    data = None
    db_name_input = request.form.get('DbName')
    sql_text = request.form.get('SqlText')
    sql_type = checktype.lower()

#   判断数据库类型,如果是垂直拆分的数据库,则返回第一个库的DbName
    schema_info = SchemaList.query.filter_by(name=db_name_input).first()
    sub_schema_info = SchemaList.query.filter_by(parent_id=schema_info.id).first()
    if sub_schema_info:
        db_name = sub_schema_info.name
    else:
        db_name = db_name_input

    if sql_type in ('ddl', 'dml'):
        sqlreview = SqlReview()
        ReviewResult = sqlreview.SqlReview(db_name, sql_text, sql_type)
        status = ReviewResult['status']
        msg = ReviewResult['msg']
        data = ReviewResult['data']

    else:
        status = -1
        msg = '未知的校验类型!'

    return jsonify(status=status, msg=msg, data=data)
