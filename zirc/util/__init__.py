import inspect, threading
from . import colors

def function_argument_call(func, arguments, do_thread=True):
    try:
        accepts = inspect.getargspec(func)[0]
    except TypeError:
        accepts = inspect.getargspec(func.__init__)[0]
    x = {}
    for val, arg in enumerate(accepts):
        if val == 0 and (inspect.ismethod(func) or inspect.isclass(func)):
            continue  # Ingnore first argument if it is a method
        x[arg] = arguments.get(arg, None)
    if do_thread:
        thread = threading.Thread(target=func, kwargs=x)
        thread.daemon = True
        return thread.start
    call_func = lambda: func(**x)
    return call_func
