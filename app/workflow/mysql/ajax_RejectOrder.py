# -*-coding: utf-8-*-
from flask import jsonify, request, session
from flask_login import current_user
from . import workflow_mysql
from app.models import OrderStatus, OrderList, OrderMysqlDDLInfo, \
                    OrderMysqlDMLInfo
from app.mysql.SqlReview import SqlReview
from app.redis import CounterOrderId
from app import db


@workflow_mysql.route('/rejectorder/<order_type>', methods=['GET', 'POST'])
def MysqlRejectOrder(order_type):
    status = 1
    msg = ""

#   从js获取表单
    order_id = request.form.get('OrderId')
    order_title = request.form.get('OrderTitle')
    db_name = request.form.get('DbName')
    remark_text = request.form.get('RemarkText')
    sql_text = request.form.get('SqlText')
    owner_id = request.form.get('OwnerId')
    dba_suggest = request.form.get('DBASuggest')

    auditor_id = current_user.get_id()

#   修改order_list表的状态已经当前处理用户
    order_status_id = OrderStatus.query.filter_by(name=u'用户修改').first().id
    order_info = OrderList.query.filter_by(order_id=order_id).first()
    order_info.order_status = order_status_id
    order_info.current_user_id = order_info.owner_id

#   order_detail表:将原来的那条状态值非-1的数据,状态改成-1,并插入一条新的数据
    if order_type == 'ddl':
        order_detail_info = OrderMysqlDDLInfo.query.filter(OrderMysqlDDLInfo.order_id == order_id)
        order_detail_info = order_detail_info.filter(OrderMysqlDDLInfo.order_status != -1).first()
        order_detail_info.order_status = -1

        new_detail_info = OrderMysqlDDLInfo(owner_id=owner_id,
                                            order_id=order_id,
                                            order_title=order_title,
                                            db_name=db_name,
                                            remark_text=remark_text,
                                            sql_text=sql_text,
                                            auditor_id=auditor_id,
                                            current_user_id=auditor_id,
                                            order_status=order_status_id,
                                            dba_suggest=dba_suggest)
    elif order_type == 'dml':
        order_detail_info = OrderMysqlDMLInfo.query.filter(OrderMysqlDMLInfo.order_id == order_id)
        order_detail_info = order_detail_info.filter(OrderMysqlDMLInfo.order_status != -1).first()
        order_detail_info.order_status = -1
        is_backup = request.form.get('NeedBackup')

        new_detail_info = OrderMysqlDMLInfo(owner_id=owner_id,
                                            order_id=order_id,
                                            order_title=order_title,
                                            db_name=db_name,
                                            remark_text=remark_text,
                                            sql_text=sql_text,
                                            is_backup=is_backup,
                                            auditor_id=auditor_id,
                                            current_user_id=auditor_id,
                                            order_status=order_status_id,
                                            dba_suggest=dba_suggest)

    db.session.add(new_detail_info)
    db.session.commit()

    db.session.commit()

    return jsonify(status=status, msg=msg)
