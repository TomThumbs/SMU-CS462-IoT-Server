from flask import Blueprint, request
import json
import common

missing_api = Blueprint('missing_api', __name__)

@missing_api.route('/getAllMissingOccurences', methods=['GET'])
def getAllMissingOccurences():
    missing = common.database_connection('select * from missing_occurences', 'select')
    return json.dumps(missing)

@missing_api.route('/getMissingOccurence', methods=['GET'])
def getMissingOccurence():
    bid = request.args.get('bid')
    missing = common.database_connection('select * from missing_occurences where bid = %s', 'select',bid)
    return json.dumps(missing)

# @missing_api.route('/getLastMissingOccurence', methods=['GET'])
# def getLastMissingOccurence():
#     missing = common.database_connection('select * from missing_occurences order_by id desc limit 1', 'select')
#     return json.dumps(missing)