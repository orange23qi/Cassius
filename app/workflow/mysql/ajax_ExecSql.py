# -*-coding: utf-8-*-
from flask import jsonify, request, session
from app.mysql.Inception import Inception
from app.models import OrderList, OrderMysqlDDLInfo, OrderStatus, \
                    OrderMysqlDMLInfo
from app import db
from . import workflow_mysql


@workflow_mysql.route('/execsql/<review_type>', methods=['GET', 'POST'])
def ExecSql(review_type):
    status = 1
    msg = ''

    db_name = request.form.get('DbName')
    sql_text = request.form.get('SqlText')
    order_id = request.form.get('OrderId')

    inception = Inception()
    if review_type == 'ddl':
        result = inception.InceptionExecuteDDL(db_name, sql_text)

    elif review_type == 'dml':
        is_backup = request.form.get('NeedBackup')
        result = inception.InceptionExecuteDML(db_name, sql_text, is_backup)

    if result['status'] == -1:
        status = result['status']
        msg = result['msg']
        return jsonify(status=status, msg=msg)

    order_status_id = OrderStatus.query.filter_by(name=u'已完成').first().id
    order_info = OrderList.query.filter_by(order_id=order_id).first()
    order_info.current_user_id = -1
    order_info.order_status = order_status_id

    if review_type == 'ddl':
        detail_info = OrderMysqlDDLInfo.query.filter(OrderMysqlDDLInfo.order_id == order_id)
        detail_info = detail_info.filter(OrderMysqlDDLInfo.order_status != -1).first()

    elif review_type == 'dml':
        detail_info = OrderMysqlDMLInfo.query.filter(OrderMysqlDMLInfo.order_id == order_id)
        detail_info = detail_info.filter(OrderMysqlDMLInfo.order_status != -1).first()

    detail_info.current_user_id = -1
    detail_info.order_status = order_status_id

    db.session.commit()

    return jsonify(status=status, msg=msg)