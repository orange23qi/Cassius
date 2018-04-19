# -*-coding: utf-8-*-
from flask import current_app
import redis


def RedisExcept(RedisCommand):
    def warpper(*args, **kwargs):
        status = 1
        msg = ''
        result = None

        try:
            result = RedisCommand(*args, **kwargs)

        except redis.exceptions.RedisError as e:
            status = -1
            msg = "Redis Error : %s" % e
            print msg
            return {'status': status, 'msg': msg, 'data': result}

        return {'status': status, 'msg': msg, 'data': result}

    return warpper


class RedisDao(object):
    def __init__(self):
        app = current_app._get_current_object()

        self.RedisHost = app.config['REDIS_HOST']
        self.RedisPort = int(app.config['REDIS_PORT'])
        self.RedisDb = int(app.config['REDIS_DB'])

        self.Conn = None
        self.Conn = redis.StrictRedis(host=self.RedisHost,
                                      port=self.RedisPort,
                                      db=self.RedisDb)

    @RedisExcept
    def RedisSet(self, RedisKey, RedisValue):
        result = None
        """
        if RedisTtl is None or RedisTtl == '':
            RedisTtl = 60
        result = self.Conn.set(RedisKey, RedisValue, RedisTtl)
        """
        result = self.Conn.set(RedisKey, RedisValue)
        return result

    @RedisExcept
    def RedisGet(self, RedisKey):
        result = None
        result = self.Conn.get(RedisKey)
        return result

    @RedisExcept
    def RedisDel(self, RedisKey):
        result = None
        result = self.Conn.delete(RedisKey)
        return result

    @RedisExcept
    def RedisRename(self, RedisKey, RedisNewKey):
        result = None
        result = self.Conn.rename(RedisKey, RedisNewKey)
        return result

    @RedisExcept
    def RedisIncr(self, RedisKey):
        result = None
        result = self.Conn.incr(RedisKey)
        return result

    @RedisExcept
    def RedisExists(self, RedisKey):
        result = None
        result = self.Conn.exists(RedisKey)
        return result
