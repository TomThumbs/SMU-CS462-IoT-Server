#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = "ubuntu"
DB_USERNAME = "ubuntu"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
# DB_HOST = "3.132.83.5"

# threshold = 5 * 60

def database_connection(query, querytype, *args):
    try:
        # con = psycopg2.connect(database="IoT-CS462", user="jamesedwardteoh", password="", host="127.0.0.1")
        con = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
        print("Database opened sucessfully")

        cur = con.cursor(cursor_factory=RealDictCursor)
        # query = "select * from user_details"
        cur.execute(query, args)

        if (querytype == "select"):
            rows = cur.fetchall()
            # for row in rows:
            #     print(row)
        elif(querytype == "insert" or querytype == "update"):
            con.commit()
            rows = None
    
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        if (con):
            return rows
            cur.close()
            con.close()
            print("PostgreSQL connection is closed")

database_connection('delete from last_seen', 'update')