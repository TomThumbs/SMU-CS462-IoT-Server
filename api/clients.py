from flask import Blueprint, request
import common
import json

client_api = Blueprint('client_api', __name__)

@client_api.route('/getAllClients', methods=['GET'])
def getAllClients():
    rows = common.database_connection("Select * from client_details", "select")
    return json.dumps(rows)

@client_api.route('/getClient', methods=['GET'])
def getClient():
    bid = request.args.get('bid')
    rows = common.database_connection("select * from client_details where bid = %s", 'select', bid)
    return json.dumps(rows)