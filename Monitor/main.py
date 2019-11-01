import psutil
import time
import pymongo
import redis

REDIS = {'host': '172.17.0.2', 'port': 6379, 'db': 10, 'password': 'Aa12345'}
pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'])
MONGO = 'mongodb://%s:%s@%s:%s/' % ('root', 'Aa12345!', '172.17.0.3', '27017')


# REDIS = {'host': '127.0.0.1', 'port': 6379, 'db': 10}
# pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'])
# MONGO = 'mongodb://%s:%s/' % ('127.0.0.1', '27017')


class Record:
    r = redis.StrictRedis(connection_pool=pool)
    conn = pymongo.MongoClient(MONGO)
    net = dict()

    def __init__(self):
        self.cpu_count_physical = psutil.cpu_count(logical=False)
        self.cpu_count_logical = psutil.cpu_count()

    def record_cpu(self, threshold=10, mongo=500, delete=150):
        cpu_percent = psutil.cpu_percent()
        cpu = {'cpu_count_physical': self.cpu_count_physical, 'cpu_count_logical': self.cpu_count_logical,
               'cpu_percent': cpu_percent, 'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        self.r.rpush('cpu', str(cpu))
        if self.r.llen('cpu') > threshold:
            self.r.blpop('cpu')
        self.conn['monitor']['cpu'].insert_one(cpu)
        if self.conn['monitor']['cpu'].count_documents({}) > mongo:
            tmp = []
            for i in self.conn['monitor']['cpu'].find().limit(delete):
                tmp.append(i)
            self.conn['monitor']['cpu'].delete_many({'$or': tmp})

    def record_memory(self, threshold=10, mongo=500, delete=150):
        tmp = psutil.virtual_memory()
        memory = {'memory_total': tmp.total, 'memory_used': tmp.used, 'memory_percent': tmp.percent,
                  'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        print(memory)
        self.r.rpush('memory', str(memory))
        if self.r.llen('memory') > threshold:
            self.r.blpop('memory')
        self.conn['monitor']['memory'].insert_one(memory)
        if self.conn['monitor']['memory'].count_documents({}) > mongo:
            tmp = []
            for i in self.conn['monitor']['memory'].find().limit(delete):
                tmp.append(i)
            self.conn['monitor']['memory'].delete_many({'$or': tmp})

    def record_disk(self, threshold=10, mongo=500, delete=150):
        disk = dict()
        for i in psutil.disk_partitions():
            tmp = psutil.disk_usage(i.mountpoint)
            disk[i.mountpoint] = {'disk_total': tmp.total, 'disk_used': tmp.used, 'disk_free': tmp.free,
                                  'disk_percent': tmp.percent,
                                  'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        self.r.rpush('disk', str(disk))
        if self.r.llen('disk') > threshold:
            self.r.blpop('disk')
        self.conn['monitor']['disk'].insert_one(disk)
        if self.conn['monitor']['disk'].count_documents({}) > mongo:
            tmp = []
            for i in self.conn['monitor']['disk'].find().limit(delete):
                tmp.append(i)
            self.conn['monitor']['disk'].delete_many({'$or': tmp})

    def record_disk_io(self, threshold=10, mongo=500, delete=150):
        disk_io = dict()
        tmp = psutil.disk_io_counters(perdisk=True)
        for i in tmp:
            disk_io[i] = {'read_bytes': tmp[i].read_bytes, 'write_bytes': tmp[i].write_bytes,
                          'read_time': tmp[i].read_time,
                          'write_time': tmp[i].write_time,
                          'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        self.r.rpush('disk_io', str(disk_io))
        if self.r.llen('disk_io') > threshold:
            self.r.blpop('disk_io')
        self.conn['monitor']['disk_io'].insert_one(disk_io)
        if self.conn['monitor']['disk_io'].count_documents({}) > mongo:
            tmp = []
            for i in self.conn['monitor']['disk_io'].find().limit(delete):
                tmp.append(i)
            self.conn['monitor']['disk_io'].delete_many({'$or': tmp})

    def record_net(self, threshold=10, mongo=500, delete=150):
        net = dict()
        network = dict()
        tmp = psutil.net_io_counters(pernic=True)
        for i in tmp:
            if i in self.net:
                network[i] = {'bytes_sent': tmp[i].bytes_sent - self.net[i]['bytes_sent'],
                              'bytes_recv': tmp[i].bytes_recv - self.net[i]['bytes_recv']}
            net[i] = {'bytes_sent': tmp[i].bytes_sent, 'bytes_recv': tmp[i].bytes_recv}
        self.net = net
        if 'eth0' in network:
            self.r.rpush('network',
                         str({'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'network': network}))
            if self.r.llen('network') > threshold:
                self.r.blpop('network')
            self.conn['monitor']['network'].insert_one(
                {'date_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'network': network})
            if self.conn['monitor']['network'].count_documents({}) > mongo:
                tmp = []
                for i in self.conn['monitor']['network'].find().limit(delete):
                    tmp.append(i)
                self.conn['monitor']['network'].delete_many({'$or': tmp})


def run(pause=5, threshold=20):
    record = Record()
    r = redis.StrictRedis(connection_pool=pool)
    count = 60
    while True:
        # if count >= 60:
        #     record.record_disk(threshold)  # DISK 监控状态
        #     count = 0

        record.record_disk(threshold)  # DISK 监控状态
        record.record_cpu(threshold)  # CPU 监控状态
        record.record_memory(threshold)  # MEMORY 监控状态
        record.record_net(threshold)  # NETWORK 监控状态
        record.record_disk_io(threshold)  # DISK_IO 监控状态
        count += pause
        print(type(r.lrange('cpu', 0, -1)), r.lrange('cpu', 0, -1))
        time.sleep(pause)


if __name__ == '__main__':
    run()
