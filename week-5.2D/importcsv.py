import pymongo
import pandas as pd

MONGO_URI = "mongodb+srv://SumitGrover:Sumit123@cluster95.xr9kt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster95"
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["sensor_data"]
collection = db["gyroscope"]

data = list(collection.find({}))
df = pd.DataFrame(data)
df.drop(columns=['_id'], inplace=True)

csv_filename = "gyroscope_data.csv"
df.to_csv(csv_filename, index=False)

print(f"Data exported to {csv_filename}")
