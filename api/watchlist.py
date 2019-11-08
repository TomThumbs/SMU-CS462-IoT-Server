from flask import Blueprint
import common
import json

watchlist_api = Blueprint('watchlist_api', __name__)

@watchlist_api.route('/getWatchlist', methods=['GET'])
def getWatchlist():
    rows = common.database_connection('select * from watch_list', 'select')
    return json.dumps(rows)