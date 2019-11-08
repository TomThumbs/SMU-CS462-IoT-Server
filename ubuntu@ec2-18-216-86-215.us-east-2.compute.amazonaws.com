import paho.mqtt.client as mqtt
import psycopg2
import json
import logging

# DB_NAME = "IoT-CS462"
# DB_USERNAME = "jamesedwardteoh"
# DB_PASSWORD = ""
# DB_HOST = "127.0.0.1"

LOG_FILENAME = "output.log"

DB_NAME = "ubuntu"
DB_USERNAME = "ubuntu"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"

MQTT_TOPIC = "potato"

logging.basicConfig(filename=LOG_FILENAME ,level=logging.INFO,
                    format="[%(asctime)s] (%(levelname)s) %(message)s")

# Callbacks
def on_connect( client, userdata, flags, rc):
    logging.info("Connected with Code : " + str(rc))
    client.subscribe(MQTT_TOPIC, 1)

# def on_message( client, userdata, msg):
#     payload = msg.payload
#     # print(payload)
#     payload = payload.decode('UTF-8')
#     # print(payload)
#     payload = json.loads(payload)
#     database_connection("insert into raw_data(bid, timestamp, receiverid) values (%s, %s, %s)", "insert", payload['bid'], payload['timestamp'], payload['receiverid'])

def on_message( client, userdata, msg):
    logging.info("Received message...")
    payload = msg.payload
    payload = payload.decode('UTF-8')
    
    payload = json.loads(payload)
    database_connection("insert into raw_data (bid, timestamp, receiverid) values (%s, %s, %s)", "insert", payload['bid'], payload['timestamp'], payload['receiverid'])
    check = database_connection("Select * from last_seen where bid = %s", "select", payload['bid'])
    
    if check == []:
        database_connection("insert into last_seen(bid, timestamp, receiverid) values (%s, %s, %s)", "insert", payload['bid'], payload['timestamp'], payload['receiverid'])
    else:
        database_connection("""update last_seen 
                                set timestamp = %s, 
                                    receiverid = %s 
                                where bid = %s""", "update", payload['timestamp'], payload['receiverid'], payload['bid'])
    
    logging.info("Successfully processed message!")

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

client.connect("soldier.cloudmqtt.com", 11260)
client.username_pw_set("yrnbfcpz", "En09Pm6ARWAa")

client.loop_forever()