import paho.mqtt.client as mqtt
import psycopg2
import json
import logging
from datetime import datetime, timedelta

# DB_NAME = "IoT-CS462"
# DB_USERNAME = "jamesedwardteoh"
# DB_PASSWORD = ""

DB_NAME = "ubuntu"
DB_USERNAME = "ubuntu"
DB_PASSWORD = "12345678"

DB_HOST = "127.0.0.1"

LOG_FILENAME = "output.log"

# LOG_FILENAME = "cloud_output.log"

MQTT_TOPIC = "potato"

logging.basicConfig(filename=LOG_FILENAME ,level=logging.INFO,
                    format="[%(asctime)s] (%(levelname)s) %(message)s")

# Callbacks
def on_connect( client, userdata, flags, rc):
    # print("Connected with Code : " + str(rc))
    logging.info("Connected with Code : " + str(rc))
    client.subscribe(MQTT_TOPIC, 1)

def on_message( client, userdata, msg):
    logging.info("Received message...")
    payload = msg.payload
    payload = payload.decode('UTF-8')
    
    logging.info(payload)
    payload = json.loads(payload)

    # extract data from payload
    bid = payload['bid']
    # print(bid)

    timestamp = payload['timestamp']
    dt = datetime.fromtimestamp(timestamp * 0.001)
    # dt = dt + timedelta(hours=8)
    date_time = dt.strftime("%d/%m/%Y %H:%M:%S")
    # print(date_time)

    receiverid = payload['receiverid']
    # print(receiverid)
    # print()
    
    # insert into raw data table
    database_connection("insert into raw_data (bid, timestamp, receiverid) values (%s, %s, %s)", "insert", bid, date_time, receiverid)
    
    # insert into daily attendance
    date = dt.strftime("%d/%m/%Y")
    # database_connection("insert into daily_attendance (bid, date) values (%s, %s)", 'insert', bid, dt.strftime("%d/%m/%Y"))
    database_connection("insert into daily_attendance (bid, date) select %s, %s where not exists (select * from daily_attendance where bid = %s and date = %s)", 'insert', bid, date, bid, date)
    
    # Checks whether client has been seen today
    check = database_connection("Select * from last_seen where bid = %s", "select", bid)
    
    if check == []:
        # Add new client into last seen table
        database_connection("insert into last_seen(bid, timestamp, receiverid) values (%s, %s, %s)", "insert", bid, date_time, receiverid)
    else:
        # Update client's last seen time
        database_connection("""update last_seen 
                                set timestamp = %s, 
                                    receiverid = %s 
                                where bid = %s""", "update", date_time, receiverid, bid)
    
    logging.info("Successfully processed message!")

# Database connection and query
def database_connection(query, type,*args):
    try:
        con = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)

        cur = con.cursor()
        # query = "select * from user_details"
        cur.execute(query, args)

        if (type == "select"):
            rows = cur.fetchall()
            # for row in rows:
            #     print(row)
        elif(type == "insert" or type == "update"):
            con.commit()
            rows = None
    
    except (Exception, psycopg2.Error) as error:
        logging.error("Error fetching data from PostgreSQL table", error)

    finally:
        if (con):
            return rows 
            cur.close()
            con.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("soldier.cloudmqtt.com", 11260)
# client.username_pw_set("yrnbfcpz", "En09Pm6ARWAa")
client.connect("broker.mqttdashboard.com", 1883)

client.loop_forever()