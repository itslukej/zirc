from .connection import Socket
from .event import Event

class NoSocket(Exception):
    pass

class Client(object):
    def connect(self, address, port=6667):
        self.socket = self.connection((address, port))
    def recv(self):
        self.part = ""
        self.data = ""
        while not self.part.endswith("\r\n"):
            self.part = self.socket.recv(2048)
            self.part = self.part.decode("UTF-8", "ignore")
            self.data += self.part
        self.data = self.data.strip().split("\r\n")
        return self.data
    def start(self):
        while True:
            for query in self.recv():
                event = Event(query)
                func_name = "on_"+event.type.lower()
                if hasattr(self, func_name):
                    getattr(self, func_name)(event)
                if hasattr(self, "on_all"):
                    self.on_all(event)