from flask import Blueprint, request
import json
import common

staff_api = Blueprint('staff_api', __name__)

@staff_api.route('/getAllStaffs', methods=['GET'])
def getAllStaffs():
    rows = common.database_connection('select * from staff_details', 'select')
    return json.dumps(rows)

@staff_api.route('/getStaff')
def getStaff(name):
    name = request.args.get('name')
    rows = common.database_connection("select * from staff_details where name like '%%%s%%'", 'select', name)
    return json.dumps(rows)