# -*-coding: utf-8-*-
from flask import jsonify, request, current_app
from functools import wraps
from . import api


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args, **kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)

    return decorated_function


@api.route('/userlogin', methods=['POST', 'GET'])
@support_jsonp
def UserLogin():
    data = "true"
    print "UserLogin API:", jsonify(data=data)
    return jsonify(data=data)