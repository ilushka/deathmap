import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'normal', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

rq_connection = redis.from_url(redis_url)

if __name__ == '__main__':
  with Connection(rq_connection):
    worker = Worker(map(Queue, listen))
    worker.work()

