import paho.mqtt.client as mqtt
import json
import couchdb
from datetime import datetime

couch = couchdb.Server("http://127.0.0.1:5984/")
couch.resource.credentials = ("Sumit", "Sumit123")

db_name = "gyro"
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())  
    timestamp = datetime.now().isoformat() 

    db.save({
        "_id": timestamp,  
        "sensor_name": payload["sensor_name"],
        "timestamp": payload["timestamp"],
        "x": payload["x"],
        "y": payload["y"],
        "z": payload["z"]
    })

    print(f" Data Inserted into CouchDB: {payload}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
client.on_message = on_message
client.username_pw_set("sumitgrover", "Kller@257")  
client.tls_set()  
client.connect("4792689a80ea4a7da929c87ea9ef7bd2.s1.eu.hivemq.cloud", 8883)
client.subscribe("sensor/gyroscope")
client.loop_forever()