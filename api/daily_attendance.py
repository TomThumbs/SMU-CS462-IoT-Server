import common
from flask import Blueprint, request
import json

attendance_api = Blueprint('attendance_api', __name__)

@attendance_api.route('/getAllAttendance', methods=['GET'])
def getAllAttendance():
    attendance = common.database_connection('select * from daily_attendance', 'select')
    return json.dumps(attendance)