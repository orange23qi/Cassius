# -*-coding: utf-8-*-
from app.models import OrderList
from app import db
from sqlalchemy import func
from . import RedisDao
import time


class CounterOrderId(object):
    def __init__(self):
        self.LockName = 'lock|order_id'
        self.LockCountNum = 5
        self.KeyName = 'counter|order_id'

    def CounterOrderId(self):
        status = 1
        msg = ''
        data = None

        redisdao = RedisDao.RedisDao()
        IfLockExists = redisdao.RedisExists(self.LockName)
        status = IfLockExists['status']
        if status == -1:
            msg = IfLockExists['msg']
            return {'status': status, 'msg': msg, 'data': data}

        if IfLockExists is True:
            count = 0
            while count < self.LockCountNum:
                time.sleep(0.1)
                IfLockExists = redisdao.RedisExists(self.LockName)
                status = IfLockExists['status']
                if status == -1:
                    msg = IfLockExists['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                if IfLockExists is False:
                    count = self.LockCountNum + 1
                else:
                    count += 1

            if count == self.LockCountNum:
                status = -1
                msg = "获取订单号锁等待超时."
                return {'status': status, 'msg': msg, 'data': data}

        """
        如果不存在锁,则开始获取key的值
        首先判断key存不存在
        """
        IfExists = redisdao.RedisExists(self.KeyName)
        status = IfExists['status']
        if status == -1:
            msg = IfExists['msg']
            return {'status': status, 'msg': msg, 'data': data}

        if IfExists['data'] is True:
            """
            如果存在则直接获取值,并自增1
            """
            LockSet = redisdao.RedisSet(self.LockName, 1)
            status = LockSet['status']
            if status == -1:
                msg = LockSet['msg']
                return {'status': status, 'msg': msg, 'data': data}

            GetResult = redisdao.RedisGet(self.KeyName)
            status = GetResult['status']
            if status == -1:
                msg = GetResult['msg']
                return {'status': status, 'msg': msg, 'data': data}
            data = GetResult['data']

            IncrResult = redisdao.RedisIncr(self.KeyName)
            status = IncrResult['status']
            if status == -1:
                msg = IncrResult['msg']
                return {'status': status, 'msg': msg, 'data': data}

            LockDel = redisdao.RedisDel(self.LockName)
            status = LockDel['status']
            if status == -1:
                msg = LockDel['msg']
                return {'status': status, 'msg': msg, 'data': data}

            return {'status': status, 'msg': msg, 'data': data}

        else:
            """
            如果key不存在,则直接到数据库中获取
            """
            OrderId = OrderList.query.order_by(db.desc(OrderList.id)).first()

            if OrderId is None:
                OrderId = 1
                data = OrderId

                LockSet = redisdao.RedisSet(self.LockName, 1)
                status = LockSet['status']
                if status == -1:
                    msg = LockSet['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                SetResult = redisdao.RedisSet(self.KeyName, OrderId)
                status = SetResult['status']
                if status == -1:
                    msg = SetResult['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                LockDel = redisdao.RedisDel(self.LockName)
                status = LockDel['status']
                if status == -1:
                    msg = LockDel['msg']
                    return {'status': status, 'msg': msg, 'data': data}

            else:
                data = OrderId

                LockSet = redisdao.RedisSet(self.LockName, 1)
                status = LockSet['status']
                if status == -1:
                    msg = LockSet['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                SetResult = redisdao.RedisSet(self.KeyName, OrderId + 1)
                status = SetResult['status']
                if status == -1:
                    msg = SetResult['msg']
                    return {'status': status, 'msg': msg, 'data': data}

                LockDel = redisdao.RedisDel(self.LockName)
                status = LockDel['status']
                if status == -1:
                    msg = LockDel['msg']
                    return {'status': status, 'msg': msg, 'data': data}

            return {'status': status, 'msg': msg, 'data': data}
