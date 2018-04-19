# -*-coding: utf-8-*-
from flask import jsonify, request
from . import workflow
from app.models import DBATeam


@workflow.route('/dbalist/', methods=['GET', 'POST'])
def GetDBAList():
    """
    获取DBA列表
    """
    data = []
    Users = DBATeam.query.all()
    for row in Users:
        data.append(row.name)

    return jsonify(data=data)
