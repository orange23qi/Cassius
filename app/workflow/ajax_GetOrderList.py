# -*-coding: utf-8-*-
from flask import jsonify, request, session
from flask_login import current_user
from . import workflow
from .IsDBA import IsDBA
from app.models import OrderStatus, OrderList, User, OrderType
from app import db


@workflow.route('/orderlist/<QueryOrderType>', methods=['GET', 'POST'])
def GetOrderList(QueryOrderType):
    """
    根据用户获取用户的工单列表
    """
    data = []
    UserId = current_user.get_id()
    StatusId = OrderStatus.query.filter_by(name=u"已完成").first().id
    StatusRejectId = OrderStatus.query.filter_by(name=u"废弃").first().id
    isdba = IsDBA()
    DBAResult = isdba.CheckDBAUseId(UserId)

    if QueryOrderType == "todo":
        Orders = OrderList.query.filter(OrderList.current_user_id == UserId)
        Orders = Orders.filter(OrderList.order_status != StatusId).all()

    elif QueryOrderType == "doing":
        Orders = OrderList.query.filter(OrderList.owner_id == UserId)
        Orders = Orders.filter(OrderList.order_status != StatusId)
        Orders = Orders.filter(OrderList.order_status != StatusRejectId).all()

    elif QueryOrderType == "finish":
        if DBAResult['data'] == 1:
            Orders = OrderList.query.filter(OrderList.auditor_id == UserId)
            Orders = Orders.filter(OrderList.order_status == StatusId).all()

        else:
            Orders = OrderList.query.filter(OrderList.owner_id == UserId)
            Orders = Orders.filter(OrderList.order_status == StatusId).all()

    elif QueryOrderType == "all":
        if DBAResult['data'] == 1:
            Orders = OrderList.query.all()
        else:
            Orders = OrderList.query.filter(OrderList.owner_id == UserId).all()

    for row in Orders:
        RowList = []
        OrderId = row.order_id
        OrderTitle = row.order_title

        StatusForOrder = OrderStatus.query.filter_by(id=row.order_status)
        StatusForOrder = StatusForOrder.first().name

        if StatusForOrder == u"已完成":
            CurrentUser = "-"

        elif row.current_user_id == -1:
            CurrentUser = "-"

        else:
            CurrentUser = User.query.filter_by(id=row.current_user_id).first()
            CurrentUser = CurrentUser.username

        TypeForOrder = OrderType.query.filter_by(id=row.order_type).first()
        TypeForOrder = TypeForOrder.name

        CreateTime = row.create_time.strftime('%Y-%m-%d')
        Owner = User.query.filter_by(id=row.owner_id).first().username

        RowList.append(OrderId)
        RowList.append(OrderTitle)
        RowList.append(TypeForOrder)
        RowList.append(StatusForOrder)
        RowList.append(CurrentUser)
        RowList.append(Owner)
        RowList.append(CreateTime)

        data.append(RowList)

    return jsonify(data=data)
