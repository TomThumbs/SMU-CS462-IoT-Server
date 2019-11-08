from flask import Blueprint, request
import json
import common

fees_api = Blueprint('fees_api', __name__)

@fees_api.route('/getFeeTypes', methods=['GET'])
def getFeeTypes():
    rows = common.database_connection("select * from elderly_fees", 'select')
    return json.dumps(rows)

@fees_api.route('/getFee', methods=['GET'])
def getFee(feetype):
    feetype = request.args.get('feetype')
    rows = common.database_connection("select * from elderly_fees where condition = %s", 'select', feetype)
    return json.dumps(rows)