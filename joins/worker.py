import os

#=====================Running Django code locally=========================
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newworld.settings")
application = get_wsgi_application()
#========================================================================


import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')


conn = redis.from_url(redis_url)


def checkRedis(cache):
    if not conn.exists(cache):
        conn.set(cache,True)
        conn.expire(cache,3600)
        return False
    else: print 'Expire in ',conn.TTL(cache)
    return conn.exists(cache)

if __name__ == '__main__':
    with Connection(conn):
        worker=Worker(map(Queue,listen))
        worker.work()

