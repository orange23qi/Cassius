# -*-coding: utf-8-*-
from flask import jsonify
from flask_login import current_user
from app.models import OrderStatus, User, OrderMysqlDDLInfo, \
                    OrderMysqlDMLInfo
from . import workflow_mysql


@workflow_mysql.route('/orderdetail/<review_type>/<order_id>', methods=['GET'])
def OrderDetailDDL(review_type, order_id):
    data = []
    if review_type == 'ddl':
        row_info = OrderMysqlDDLInfo.query.filter(OrderMysqlDDLInfo.order_id == order_id)
        row_info = row_info.filter(OrderMysqlDDLInfo.order_status != -1).first()
    elif review_type == 'dml':
        row_info = OrderMysqlDMLInfo.query.filter(OrderMysqlDMLInfo.order_id == order_id)
        row_info = row_info.filter(OrderMysqlDMLInfo.order_status != -1).first()

    order_title = row_info.order_title
    db_name = row_info.db_name
    remark_text = row_info.remark_text
    sql_text = row_info.sql_text
    status_id = row_info.order_status
    auditor_id = row_info.auditor_id
    owner_id = row_info.owner_id
    status = OrderStatus.query.filter_by(id=status_id).first().name
    auditor = User.query.filter_by(id=auditor_id).first().username
    owner = User.query.filter_by(id=owner_id).first().username
    now_user = User.query.filter_by(id=current_user.get_id()).first().username
    order_id = row_info.order_id
    owner_id = owner_id
    dba_suggest = row_info.dba_suggest

    data.append(order_title)
    data.append(db_name)
    data.append(remark_text)
    data.append(sql_text)
    data.append(status)
    data.append(owner)
    data.append(auditor)
    data.append(now_user)
    data.append(order_id)
    data.append(owner_id)
    data.append(dba_suggest)

    if review_type == 'dml':
        is_backup = row_info.is_backup
        data.append(is_backup)

    return jsonify(data=data)