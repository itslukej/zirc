from collections import OrderedDict
from typing import Callable, List, Optional
from . import util
from .event import Event

class EventLoop(object):
    def __init__(self, recv_func: Callable[[], List[str]]):
        self.jobs: OrderedDict[str, Callable[[Event]]] = OrderedDict()
        self.cycles: int = 0
        self.current_job: Optional[str] = None
        self.break_loop = False
        self.recv_func = recv_func

    def create_job(self, name: str, method: Callable[[Event]], do_thread: bool=False):
        self.jobs[name] = {"method": method, "thread": do_thread}

    def run(self):
        while True:
            try:
                for line in self.recv_func():
                    if self.break_loop:
                        break
                    for name, method in self.jobs.items():
                        self.current_job = name
                        util.function_argument_call(method["method"], {"line": line, "event": Event(line)}, method["thread"])()
                        self.current_job = None
                    self.cycles += 1
            except (KeyboardInterrupt, OSError) as e:
                raise e

    def join(self):
        """returns None when the current job is complete"""
        while self.current_job is not None:
            continue
        return
