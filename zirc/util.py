import inspect, threading

def function_argument_call(func, arguments):
    accepts = inspect.getargspec(func)[0]
    x = {}
    for val, arg in enumerate(accepts):
        if val == 0 and inspect.ismethod(func):
            continue #Ingnore first argument if it is a method
        x[arg] = arguments.get(arg, None)
    #call_func = lambda: func(**x)
    thread = threading.Thread(target=func, kwargs=x)
    thread.daemon = True
    return thread.start