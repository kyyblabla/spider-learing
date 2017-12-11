import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time


def metric(func):
    def wrapper(*args, **kw):
        t0 = time.time()
        newFunc = func(*args, **kw)
        print('%s executed in %s ms' % (func.__name__, time.time() - t0))
        return newFunc

    return wrapper


def fetch_request(url):
    result = requests.get(url)


url_list = [
    'http://www.baidu.com',
    'http://www.bing.com',
    'http://www.cnblogs.com/'
]


@metric
def test_muti_thread():
    pool = ThreadPoolExecutor(10)
    for url in url_list:
        pool.submit(fetch_request, url)
    pool.shutdown(True)


@metric
def test_muti_process():
    pool = ProcessPoolExecutor(10)
    for url in url_list:
        pool.submit(fetch_request, url)

    pool.shutdown(True)


for a in range(1, 10):
    test_muti_thread()
    test_muti_process()
    print("----")
