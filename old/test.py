import psycopg2
import json
from psycopg2.extras import RealDictCursor


def database_connection(query, querytype, *args):
    try:
        con = psycopg2.connect(database="IoT-CS462", user="jamesedwardteoh", password="", host="127.0.0.1")
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

# rows = database_connection("Select bid, timestamp, receiverid from raw_data", "select")

rows = database_connection("Select bid, timestamp, receiverid from raw_data where bid=%s", "select", "asd")

print(rows)

if rows == []:
    print("Nothing")
# print()
# print(json.dumps(rows))
# print()
# print(json.dumps(json.dumps(rows)))
# print()
print({"list": json.dumps(rows)})