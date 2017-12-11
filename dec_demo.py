import time


def timer_dec(func):
    def dec(*args, **kwargs):
        print("the %s run ..." % (func.__name__,))
        start_time = time.time()
        func(*args, **kwargs)
        print("the %s run time is %s" % (func.__name__, (time.time() - start_time)))

    return dec


@timer_dec
def funx(password):
    return "xxx"


funx("test")
