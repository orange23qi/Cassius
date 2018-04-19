from flask import Blueprint

workflow = Blueprint('workflow', __name__)

from . import views, ajax_GetDBAList, ajax_GetOrderList
