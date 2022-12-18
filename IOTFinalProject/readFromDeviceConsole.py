import datetime as dt
import time

import pymongo
import serial
from flask import jsonify, request, Flask

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://balls:balls@tempproject.zkvxtwe.mongodb.net/?retryWrites=true&w=majority")
db = client.test
data_collections = db.data

if 'weather' not in db.list_collection_names():
    db.create_collection('weather',

                         timeseries={'timeField': 'timestamp', 'metaField': 'id', 'granularity': 'seconds'}

                         )

PORT = 'COM3'
ser = serial.Serial(PORT, 9600)

humArray = []
tempArray = []
lightArray = []

#just make fields to store locally coming bits and split them
# and then append that to the new fields listed in the document
# structure


def add_collection(tempArray, humArray, lightArray):
    test_document = {
        'timestamp': dt.datetime.now(),
        'id': 1,
        'temp': tempArray,
        'humidity': humArray,
        'light levels': lightArray
    }
    data_collections.insert_one(test_document)


@app.route('/temps/', methods=["POST"])
def add_new_data():
    action = request.json['action']
    if action not in ["locked", "unlocked"]:
        return {"error", "wrong type of action submitted"}, 404

    location = request.json['location']
    userid = request.json['userid']
    add_collection(action, location, userid)
    return jsonify({"data saved": f"{location} was {action} by {userid}"})


while True:
    input = ser.readline()
    data = input.strip().decode()
    split_string = data.split(',')  # split string
    humidity = float(split_string[0])  # convert first part of string into float
    temperature = float(split_string[1])  # convert second part of string into float
    light = float(split_string[2])

    for x in humArray:
        humArray.pop(0)


    for x in tempArray:
        tempArray.pop(0)


    for x in lightArray:
        lightArray.pop(0)


    #print(humidity, temperature, light)
    humArray.append(humidity)  # add humidity values into array
    tempArray.append(temperature)  # add temperature values into array
    lightArray.append(light)
    print(humArray, tempArray, lightArray)

    if __name__ == '__main__':
        app.run()

    time.sleep(2)