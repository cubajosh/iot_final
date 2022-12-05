from flask import Flask, request, jsonify
import datetime as dt
import Emulator as em

app = Flask(__name__)
app.config['DEBUG'] = True

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


if __name__ == "__main__":
    app.run(port=5001)
