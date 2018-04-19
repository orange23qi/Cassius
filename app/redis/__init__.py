from flask import Blueprint

redis = Blueprint('redis', __name__)

from . import RedisDao, CounterOrderId
