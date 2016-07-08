import inspect, threading

def function_argument_call(func, arguments):
    accepts = inspect.getargspec(func)[0]
    x = {}
    for val, arg in enumerate(accepts):
        if val == 0 and inspect.ismethod(func):
            continue #Ingnore first argument if it is a ismethod
        if arg in arguments.keys():
            x[arg] = arguments[arg]
        else:
            x[arg] = None
    call_func = lambda: func(**x)
    thread = threading.Thread(target=call_func)
    thread.daemon = True
    return thread.start