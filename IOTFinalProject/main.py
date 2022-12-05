import pymongo as pymongo
from flask import Flask, request, jsonify
import datetime as dt

app = Flask(__name__)
app.config['DEBUG'] = True

client = pymongo.MongoClient("mongodb+srv://balls:balls@tempproject.zkvxtwe.mongodb.net/?retryWrites=true&w=majority")
db = client.test

if 'weather' not in db.list_collection_names():
    db.create_collection('weather',

                         timeseries={'timeField': 'timestamp', 'metaField': 'id', 'granularity': 'seconds'}

                         )
# dummy data to see if the conection works#
db.weather.insert_one({

    'timestamp': dt.datetime.now(),
    'id': 1,
    'temp': 32.1,
    'humidity': 87.1,
    'light levels': 150
})


def getTimeStamp():
    return dt.datetime.today().replace(microsecond=0)


@app.route("/temps/all")
def getAll():

    start = request.args.get("start")
    end = request.args.get("end")

    query = db.collection.find()
    tempList = {}

    for x in query:
        tempList = {'temps': x}

        if start is None and end is not None:
            try:
                end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
            except Exception as e:
                return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

            tempList.update({"timestamp": {"$lte": end}})

        elif end is None and start is not None:
            try:
                start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            except Exception as e:
                return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

            tempList.update({"timestamp": {"$gte": start}})
        elif start is not None and end is not None:
            try:
                start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
                end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

            except Exception as e:
                return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

            tempList.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(db.weather.aggregate([
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

    data = list(db.weather.aggregate([
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
        return {"error": "id not found, the only Id we have is 1 (for testing)"}, 404


if __name__ == "__main__":
    app.run(port=5001)
