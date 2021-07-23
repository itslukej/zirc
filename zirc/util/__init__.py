import inspect, threading
from typing import Any, Callable, Dict, Optional
from . import colors

def function_argument_call(func: Callable, arguments: Dict[str, Any], do_thread: Optional[bool]=True):
    try:
        accepts = inspect.getargspec(func)[0]
    except TypeError:
        accepts = inspect.getargspec(func.__init__)[0]
    x = {}
    for val, arg in enumerate(accepts):
        if val == 0 and (inspect.ismethod(func) or inspect.isclass(func)):
            continue  # Ingnore first argument if it is a method
        x[arg] = arguments.get(arg)
    if do_thread:
        thread = threading.Thread(target=func, kwargs=x)
        thread.daemon = True
        return thread.start
    call_func = lambda: func(**x)
    return call_func
