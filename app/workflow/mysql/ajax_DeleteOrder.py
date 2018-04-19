# -*-coding: utf-8-*-
from flask import jsonify, request
from flask_login import current_user
from app.models import OrderStatus, OrderList, OrderMysqlDDLInfo, \
                    OrderMysqlDMLInfo
from app import db
from . import workflow_mysql


@workflow_mysql.route('/deleteorder/<review_type>', methods=['GET', 'POST'])
def DelOrder(review_type):
    status = 1
    msg = ""

    order_id = request.form.get('OrderId')

    order_status_id = OrderStatus.query.filter_by(name=u'废弃').first().id
    order_info = OrderList.query.filter_by(order_id=order_id).first()
    order_info.order_status = order_status_id
    order_info.current_user_id = -1

    if review_type == 'ddl':
        detail_info = OrderMysqlDDLInfo.query.filter(OrderMysqlDDLInfo.order_id == order_id)
        detail_info = detail_info.filter(OrderMysqlDDLInfo.order_status != -1).first()
        detail_info.order_status = order_status_id
        detail_info.current_user_id = -1

    elif review_type == 'dml':
        detail_info = OrderMysqlDMLInfo.query.filter(OrderMysqlDMLInfo.order_id == order_id)
        detail_info = detail_info.filter(OrderMysqlDMLInfo.order_status != -1).first()
        detail_info.order_status = order_status_id
        detail_info.current_user_id = -1

    db.session.commit()

    return jsonify(status=status, msg=msg)