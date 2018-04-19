from flask import Blueprint

workflow_mysql = Blueprint('workflow_mysql', __name__)

from . import views, ajax_AutoReview, ajax_DeleteOrder, ajax_Submit, \
            ajax_RejectOrder, ajax_GetSchemaList, ajax_OrderDetail, \
            ajax_ExecSql
