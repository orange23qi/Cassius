# -*-coding: utf-8-*-
from app.models import User, DBATeam


class IsDBA(object):
    def __init__(self):
        self.DBAList = DBATeam.query.all()

    def CheckDBAUseId(self, UserId):
        status = 1
        msg = ""
        data = -1

        DBAIdList = []
        for DBAers in self.DBAList:
            DBAIdList.append(User.query.filter_by(username=DBAers.name).first().id)

        if UserId is None: 
            status = -1
            msg = u"用户没有登录."
            return {"status": status, "msg": msg, "data": data}

        if DBAIdList.count(long(UserId)) == 1:
            data = 1

        return {"status": status, "msg": msg, "data": data}

    def CheckDBAUseName(self, UserName):
        status = 1
        msg = ""
        data = -1

        DBAIdList = []
        for DBAers in self.DBAList:
            DBAIdList.append(DBAers.name)

        if DBAIdList.count(UserName == 1):
            data = 1

        return {"status": status, "msg": msg, "data": data}