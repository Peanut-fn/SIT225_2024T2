import couchdb
import pandas as pd
couch = couchdb.Server("http://127.0.0.1:5984/")
couch.resource.credentials = ("Sumit", "Sumit123")
db = couch["gyro"]
data = []
for doc_id in db:
    doc = db[doc_id]
    data.append({
        "timestamp": doc["_id"],
        "sensor_name": doc["sensor_name"],
        "x": doc["x"],
        "y": doc["y"],
        "z": doc["z"]
    })

df = pd.DataFrame(data)
df.to_csv("gyroscope_data_db2.csv", index=False)

print("SV File Created: gyroscope_data_db2.csv")