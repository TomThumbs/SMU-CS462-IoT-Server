#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import json
import sms

DB_NAME = "ubuntu"
DB_USERNAME = "ubuntu"
DB_PASSWORD = "12345678"
# DB_HOST = "127.0.0.1"
DB_HOST = "3.132.83.5"

# threshold = 5 * 60

def database_connection(query, querytype, *args):
    try:
        # con = psycopg2.connect(database="IoT-CS462", user="jamesedwardteoh", password="", host="127.0.0.1")
        con = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
        # print("Database opened sucessfully")

        cur = con.cursor(cursor_factory=RealDictCursor)
        # query = "select * from user_details"
        cur.execute(query, args)

        if (querytype == "select"):
            rows = cur.fetchall()
        elif(querytype == "insert" or querytype == "update"):
            con.commit()
            rows = []
    
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        if (con):
            cur.close()
            con.close()
            # print("PostgreSQL connection is closed")
            return rows

# Get all data from last_seen table of elderly's who havent gone home yet OR
# not being searched for
results = database_connection('SELECT last_seen.*, client_details.name FROM last_seen INNER JOIN client_details ON last_seen.bid = client_details.bid WHERE ((searching <> true or searching IS NULL) and (gone_home = false or gone_home IS NULL))', 'select')

# print(results)

if len(results) != 0:

    interval = database_connection('SELECT interval FROM interval_checker','select')

    threshold = interval[0]['interval'] * 60

    staffs = database_connection('SELECT * from staff_details', 'select')

    current_time = datetime.now() + timedelta(seconds=20)
    
    for result in results:
        bid = result['bid']
        timestamp = result['timestamp']
        receiverid = result['receiverid']
        name = result['name']

        # datetime from DB
        datetime_obj = datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
        date_obj = datetime_obj.strftime('%d/%m/%Y')
        time_obj = datetime_obj.strftime('%H:%M:%S')

        # time difference
        difference = None
        difference = current_time - datetime_obj
        # print(current_time)
        # print(datetime_obj)
        # print(difference.seconds)

        # checks if elderly has been gone for longer than the acceptable time limit
        if difference.seconds > threshold:
            
            # checks = database_connection('select * from watch_list where bid = %s', 'select', bid)

            # if checks == []:
            #     database_connection('insert into watch_list (bid, occurences) values (%s, 1)', 'insert', bid)
            # else:
            #     # print(check[0])
            #     for check in checks:
            #         # print(check)
            #         # occurences = int(check['occurences']) + 1
            #         database_connection('update watch_list set occurences = %s where bid = %s', 'update',int(check['occurences']) + 1, bid)
            
            # database_connection('IF NOT EXISTS (select * from missing_occurences where (bid = %s and acknowledged_timestamp IS NULL)) THEN insert into missing_occurences (bid, timestamp, receiverid) values (%s,%s,%s); END IF', 'insert', bid, bid, timestamp, receiverid)
            check = database_connection('select * from missing_occurences where bid = %s and date = %s', 'select', bid, date_obj)

            if check == []:
                database_connection('insert into missing_occurences (bid, date, time, receiverid) values (%s,%s,%s, %s)', 'insert', bid, date_obj, time_obj, receiverid)

            # database_connection('insert into missing_occurences (bid, timestamp, receiverid) values (%s,%s,%s)', 'insert', bid, timestamp, receiverid)

            # Preconfigured string for text message to be sent
            text = "Elderly {} is has gone missing at {}. Please check up on the elderly.".format(name, receiverid)

            # SMS function
            for staff in staffs:
                number = '+' + staff['contact']
                # print(text)
                sms.send_message(text, number)

        # print('end')