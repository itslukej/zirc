import inspect, threading, asyncio

def function_argument_call(func, arguments):
    try:
        accepts = inspect.getargspec(func)[0]
    except TypeError:
        accepts = inspect.getargspec(func.__init__)[0]
    x = {}
    for val, arg in enumerate(accepts):
        if val == 0 and (inspect.ismethod(func) or inspect.isclass(func)):
            continue #Ingnore first argument if it is a method
        x[arg] = arguments.get(arg, None)

    async def call_func():
        result = await func(**x)
        return result
    return call_func

