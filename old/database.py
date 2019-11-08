import psycopg2

con = psycopg2.connect(database="test", user="jamesedwardteoh", password="", host="127.0.0.1")
print("Database opened sucessfully")

cur = con.cursor()
query = "select * from user_details"
cur.execute(query)
rows = cur.fetchall()

for row in rows:
    print(row)

con.close()