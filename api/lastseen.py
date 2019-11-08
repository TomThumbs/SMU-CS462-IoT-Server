from flask import Blueprint, request
import common
import json
from datetime import datetime, timedelta

lastseen_api = Blueprint('lastseen_api', __name__)

@lastseen_api.route('/getAllLastSeen', methods=['GET'])
def getAllLastSeen():
    rows = common.database_connection("select * from last_seen", "select")
    return json.dumps(rows)

@lastseen_api.route('/resetLastSeen')
def resetLastSeen():
    common.database_connection('delete from last_seen', 'update')
    return

@lastseen_api.route('/goneHome', methods=['POST'])
def goneHome():
    bid = request.args.get('bid')
    common.database_connection('update last_seen set gone_home = TRUE where bid = %s', 'update', bid)
    return "OK"

@lastseen_api.route('/setSearching', methods=['POST'])
def setSearching():
    bid = request.args.get('bid')
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")

    # Update on last seen that client is being searched for
    common.database_connection('update last_seen set searching = TRUE where bid = %s', 'update', bid)
    # Update on missing_occurences what time it was acknowledged
    common.database_connection('update missing_occurences set acknowledged_timestamp = %s where bid = %s and acknowledged_timestamp IS NULL', 'update', current_time, bid)

    return "OK"

@lastseen_api.route('/setFound', methods=['POST'])
def setFound():
    bid = request.args.get('bid')
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")

    # Update on last seen that client has been found 
    common.database_connection('update last_seen set searching = FALSE where bid = %s', 'update', bid)
    # Update on missing_occurences what time client was found
    common.database_connection('update missing_occurences set discovered_timestamp = %s where bid = %s and discovered_timestamp IS NULL', 'update', current_time, bid)

    return "OK"