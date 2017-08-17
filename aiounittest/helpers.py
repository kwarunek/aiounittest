import asyncio
import functools


def futurized(res):
    f = asyncio.Future()
    if isinstance(res, Exception):
        f.set_exception(res)
    else:
        f.set_result(res)
    return f


def run_sync(func=None, loop=None):

    def get_brand_new_default_event_loop():
        old_loop = asyncio.get_event_loop()
        if not old_loop.is_closed():
            old_loop.close()
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
        return _loop

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal loop
            use_default_event_loop = loop is None
            if use_default_event_loop:
                loop = get_brand_new_default_event_loop()
            try:
                ret = f(*args, **kwargs)
                try:
                    future = asyncio.ensure_future(ret, loop=loop)
                except TypeError:
                    # Using `try/except` rather than iscoroutine due to support of 3.4
                    pass
                else:
                    return loop.run_until_complete(future)
            finally:
                if use_default_event_loop:
                    # clean up
                    loop.close()
                    del loop
                    # again set a new (unstopped) event loop
                    get_brand_new_default_event_loop()

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


async_test = run_sync
