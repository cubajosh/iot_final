from flask import Flask, request, jsonify
import datetime as dt
import Emulator as em
import pymongo
import datetime as dt
import random
from time import sleep

app = Flask(__name__)
app.config['DEBUG'] = True

client = pymongo.MongoClient("mongodb+srv://balls:balls@tempproject.zkvxtwe.mongodb.net/?retryWrites=true&w=majority")
db = client.test
data_collections = db.data

if 'weather' not in db.list_collection_names():
    db.create_collection('weather',

                         timeseries={'timeField': 'timestamp', 'metaField': 'id', 'granularity': 'seconds'}

                         )

def add_collection(inputId,inputTemp, inputHumidity, inputLightLevel):
    test_document = {
        'timestamp': dt.datetime.now(),
        'id': inputId,
        'temp': inputTemp,
        'humidity': inputHumidity,
        'light levels': inputLightLevel
    }
    data_collections.insert_one(test_document).inserted_id



@app.route("/temps")
def getAll():
    query = em.db.collection.find()
    tempList = {}

    for x in query:
        tempList = {'temps': x}

    data = list(em.db.weather.aggregate([
        {
            '$match': tempList
        }, {
            '$group': {
                '_id': 'none',
                'avgTemp': {
                    '$avg': '$temp'
                },
                'avgHumidity': {
                    '$avg': '$humidity'
                },
                'avgLightLevels': {
                    '$avg': '$light levels'
                },
                'Levels': {
                    '$push': {
                        'timestamp': '$timestamp',
                        'temperatures': '$temp',
                        'humidity': '$humidity',
                        'light levels': '$light levels'

                    }
                }
            }
        }
    ]))
    return data


@app.route("/temps/<int:tempId>")
def getTempById(tempId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"id": tempId}
    if start is None and end is not None:
        try:
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(em.db.weather.aggregate([
        {
            '$match': query
        }, {
            '$group': {
                '_id': '$tempId',
                'avgTemp': {
                    '$avg': '$temp'
                },
                'avgHumidity': {
                    '$avg': '$humidity'
                },
                'avgLightLevels': {
                    '$avg': '$light levels'
                },
                'temperatures': {
                    '$push': {
                        'timestamp': '$timestamp',
                        'temperatures': '$temp',
                        'humidity': '$humidity',
                        'light levels': '$light levels'

                    }
                }
            }
        }
    ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"id": tempId})

        for temp in data['temperatures']:
            temp["timestamp"] = temp["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "Id does not exist"}, 404


@app.route("/temps/humidity/<int:humidityId>")
def getHumidityById(humidityId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"id": humidityId}
    if start is None and end is not None:
        try:
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(em.db.weather.aggregate([
        {
            '$match': query
        }, {
            '$group': {
                '_id': '$humidityId',
                'humidity levels': {
                    '$push': {
                        'humidity': '$humidity',
                        'timestamp': '$timestamp'

                    }
                }
            }
        }
    ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"id": humidityId})

        for humid in data['humidity levels']:
            humid["timestamp"] = humid["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "Id does not exist"}, 404


@app.route("/temps/light/<int:lightId>")
def getLightById(lightId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"id": lightId}
    if start is None and end is not None:
        try:
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(em.db.weather.aggregate([
        {
            '$match': query
        }, {
            '$group': {
                '_id': '$lightId',
                'light levels': {
                    '$push': {
                        'light levels': '$light levels',
                        'timestamp': '$timestamp'

                    }
                }
            }
        }
    ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"id": lightId})

        for light in data['light levels']:
            light["timestamp"] = light["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "Id does not exist"}, 404


@app.route("/temps/temperatures/<int:tempId>")
def getSingleTempById(tempId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"id": tempId}
    if start is None and end is not None:
        try:
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(em.db.weather.aggregate([
        {
            '$match': query
        }, {
            '$group': {
                '_id': '$tempId',
                'Temperatures': {
                    '$push': {
                        'temperatures': '$temp',
                        'timestamp': '$timestamp'

                    }
                }
            }
        }
    ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"id": tempId})

        for temp in data['Temperatures']:
            temp["timestamp"] = temp["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "Id does not exist"}, 404

if __name__ == "__main__":
    app.run(port=5001)
