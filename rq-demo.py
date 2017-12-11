import requests
import time
from redis import Redis
from rq import Queue


def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


q = Queue(connection=Redis())

job = q.enqueue(count_words_at_url, 'http://nvie.com')

print(job.result)

# 等待一会，直到工作进程处理完
time.sleep(2)
print(job.result)
