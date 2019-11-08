from flask import Blueprint
import common
import json

rawdata_api = Blueprint('rawdata_api', __name__)

@rawdata_api.route('/getAllRawData', methods=['GET'])
def getAllRawData():
    rows = common.database_connection("select (bid, timestamp, receiverid) from raw_data", "select")
    # print (json.dumps(rows))
    return json.dumps(rows)

@rawdata_api.route('/resetRawData')
def resetRawData():
    common.database_connection('delete from raw_data', 'update')
    return