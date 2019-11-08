import common
from flask import Blueprint, request
import json

interval_api = Blueprint('interval_api',__name__)

@interval_api.route('/setInterval', methods=['POST'])
def setInterval():
    interval = request.args.get('interval')
    common.database_connection('update interval_checker set interval = %d where bid = 1', 'update', interval)
    return

@interval_api.route('/getInterval', methods=['GET'])
def getInterval():
    interval = common.database_connection('select interval from interval_checker where id = 1', 'select')
    return json.dumps(interval)