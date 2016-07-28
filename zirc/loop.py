from collections import OrderedDict
from . import util
from .event import Event

class EventLoop(object):
    def __init__(self, recv_func):
        self.jobs = OrderedDict()
        self.cycles = 0
        self.current_job = None
        self.break_loop = False
        self.recv_func = recv_func
    def create_job(self, name, method):
        self.jobs[name] = method
    def run(self):
        while True:
            for line in self.recv_func():
                if self.break_loop:
                    break
                for name, method in self.jobs.items():
                    self.current_job = name
                    util.function_argument_call(method, {"line": line, "event": Event(line)})()
                    self.current_job = None
                self.cycles += 1
    def join(self):
        """returns None when the current job is complete"""
        while self.current_job is not None:
            continue
        return