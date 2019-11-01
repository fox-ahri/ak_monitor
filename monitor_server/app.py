import redis
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


REDIS = {'host': '172.17.0.2', 'port': 6379, 'db': 10, 'password': 'Aa12345'}
pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'])
r = redis.StrictRedis(connection_pool=pool)


@app.route('/')
def hello_world():
    data = {'cpu': [], 'memory': [], 'network': [], 'disk_io': []}
    for i in r.lrange('cpu', 0, -1):
        data['cpu'].append(eval(i))
    for i in r.lrange('memory', 0, -1):
        data['memory'].append(eval(i))
    for i in r.lrange('network', 0, -1):
        data['network'].append(eval(i))
    for i in r.lrange('disk_io', 0, -1):
        data['disk_io'].append(eval(i))
    return jsonify(data)


if __name__ == '__main__':
    app.run()
