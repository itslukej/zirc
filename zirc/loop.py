from collections import OrderedDict

class ClientLoop(object):
    def __init__(self):
        self.jobs = OrderedDict()
        self.cycles = 0
        self.current_job = None
        self.break_loop = False
    def create_job(self, name, method):
        self.jobs[name] = method
    def run(self):
        while True:
            if self.break_loop:
                break
            for name, method in self.jobs.items():
                self.current_job = name
                method()
                self.current_job = None
            self.cycles += 1
    def join(self):
        """returns None when the current job is complete"""
        while self.current_job is not None:
            continue
        return