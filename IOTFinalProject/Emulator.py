import pymongo
import datetime as dt
import random
from time import sleep

client = pymongo.MongoClient("mongodb+srv://balls:balls@tempproject.zkvxtwe.mongodb.net/?retryWrites=true&w=majority")
db = client.test

sensorOn = True
loopNum = 0

if 'weather' not in db.list_collection_names():
    db.create_collection('weather',

                         timeseries={'timeField': 'timestamp', 'metaField': 'id', 'granularity': 'seconds'}

                         )

if __name__ == "__main__":
    while sensorOn:
        randomTemp = random.randint(0, 100)
        humidity = random.randint(0, 100)
        lightLevel = random.randint(0, 100)

        db.weather.insert_one({

            'timestamp': dt.datetime.now(),
            'id': 1,
            'temp': randomTemp,
            'humidity': humidity,
            'light levels': lightLevel
        })
        db.weather.insert_one({

            'timestamp': dt.datetime.now(),
            'id': 2,
            'temp': randomTemp,
            'humidity': humidity,
            'light levels': lightLevel
        })
        db.weather.insert_one({

            'timestamp': dt.datetime.now(),
            'id': 3,
            'temp': randomTemp,
            'humidity': humidity,
            'light levels': lightLevel
        })
        db.weather.insert_one({

            'timestamp': dt.datetime.now(),
            'id': 4,
            'temp': randomTemp,
            'humidity': humidity,
            'light levels': lightLevel
        })
        sleep(2)