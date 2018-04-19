# -*-coding: utf-8-*-
from flask import jsonify, request, session
from flask_login import current_user
from . import workflow_mysql
from app.models import OrderStatus, OrderList, User, OrderType, \
                    OrderMysqlDMLInfo, OrderMysqlDDLInfo, DatabaseType
from app.redis import CounterOrderId
from app import db


@workflow_mysql.route('/submit/<review_type>', methods=['GET', 'POST'])
def SubmitDDl(review_type):
    """
    提交DDL表单
    """
    status = 1
    msg = ""
    data = None

    owner_id = current_user.get_id()
    order_title = request.form.get('OrderTitle')
    db_name = request.form.get('DbName')
    remark_text = request.form.get('RemarkText')
    sql_text = request.form.get('SqlText')
    auditor = request.form.get('Auditor')
    order_id = request.form.get('OrderId')

    countorderid = CounterOrderId.CounterOrderId()

    if owner_id is not None:
        order_status_id = OrderStatus.query.filter_by(name=u'DBA审核').first().id
        db_type_id = DatabaseType.query.filter_by(name='mysql').first().id
        auditor_id = User.query.filter_by(username=auditor).first().id

        if review_type == 'ddl':
            order_type_id = OrderType.query.filter_by(name=u'MySql表结构变更').first().id
        elif review_type == 'dml':
            order_type_id = OrderType.query.filter_by(name=u'MySql数据变更').first().id
            is_backup = request.form.get('NeedBackup')

        if order_id == '':
            order_id_return = countorderid.CounterOrderId()
            if order_id_return['status'] == -1:
                msg = order_id_return['msg']
                return {'status': status, 'msg': msg, 'data': data}
            order_id = order_id_return['data']

            order_info = OrderList(order_id=order_id,
                                   owner_id=owner_id,
                                   order_title=order_title,
                                   order_type=order_type_id,
                                   db_type=db_type_id,
                                   auditor_id=auditor_id,
                                   current_user_id=auditor_id,
                                   order_status=order_status_id)

            if review_type == 'ddl':
                order_detail_info = OrderMysqlDDLInfo(owner_id=owner_id,
                                                      order_id=order_id,
                                                      order_title=order_title,
                                                      db_name=db_name,
                                                      remark_text=remark_text,
                                                      sql_text=sql_text,
                                                      auditor_id=auditor_id,
                                                      current_user_id=auditor_id,
                                                      order_status=order_status_id)

            elif review_type == 'dml':
                order_detail_info = OrderMysqlDMLInfo(owner_id=owner_id,
                                                      order_id=order_id,
                                                      order_title=order_title,
                                                      db_name=db_name,
                                                      remark_text=remark_text,
                                                      is_backup=is_backup,
                                                      sql_text=sql_text,
                                                      auditor_id=auditor_id,
                                                      current_user_id=auditor_id,
                                                      order_status=order_status_id)

            db.session.add(order_info)
            db.session.add(order_detail_info)
            db.session.commit()

        else:
            dba_suggest= request.form.get('DBASuggest')

            order_info = OrderList.query.filter_by(order_id=order_id).first()
            order_info.current_user_id = auditor_id
            order_info.order_status = order_status_id

            if review_type == 'ddl':
                order_info_detail = OrderMysqlDDLInfo.query.filter(OrderMysqlDDLInfo.order_id == order_id)
                order_info_detail = order_info_detail.filter(OrderMysqlDDLInfo.order_status != -1).first()
                order_info_detail.order_status = -1

                order_detail_info = OrderMysqlDDLInfo(owner_id=owner_id,
                                                      order_id=order_id,
                                                      order_title=order_title,
                                                      db_name=db_name,
                                                      remark_text=remark_text,
                                                      sql_text=sql_text,
                                                      auditor_id=auditor_id,
                                                      current_user_id=auditor_id,
                                                      order_status=order_status_id,
                                                      dba_suggest=dba_suggest)

            elif review_type == 'dml':
                order_info_detail = OrderMysqlDMLInfo.query.filter(OrderMysqlDMLInfo.order_id == order_id)
                order_info_detail = order_info_detail.filter(OrderMysqlDMLInfo.order_status != -1).first()
                order_info_detail.order_status = -1

                order_detail_info = OrderMysqlDMLInfo(owner_id=owner_id,
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

            db.session.add(order_detail_info)
            db.session.commit()

    else:
        status = -1
        msg = u"用户没有登录."

    return jsonify(status=status, msg=msg, data=data)
