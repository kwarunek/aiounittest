import asyncio

def futurized(res):
    f = asyncio.Future()
    if isinstance(res, Exception):
        f.set_exception(res)
    else:
        f.set_result(res)
    return f
