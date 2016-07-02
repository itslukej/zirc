from .connection import Socket
from .event import Event
from .flood import floodProtect

import sys,time

class NoSocket(Exception):
    pass

class Client(object):
    def connect(self, address, port, nickname, ident, realname, channels):
        self.fp = floodProtect()
        
        if not hasattr(self, "connection"):
            raise NoSocket("{0} has no attribute 'connection'".format(self))
        self.socket = self.connection((address, port))
        self.send("NICK {0}".format(nickname))
        self.send("USER {0} * * :{1}".format(ident, realname))
        time.sleep(5)
        for channel in channels:
            self.send("JOIN {0}".format(channel))
    def recv(self):
        self.part = ""
        self.data = ""
        while not self.part.endswith("\r\n"):
            self.part = self.socket.recv(2048)
            self.part = self.part.decode("UTF-8", "ignore")
            self.data += self.part
        self.data = self.data.strip().split("\r\n")
        return self.data
    def send(self, data):
        self.fp.queue_add(self.socket, "{0}\r\n".format(data).encode("UTF-8"))
    def start(self):
        while True:
            for query in self.recv():
                event = Event(query)
                if event.type == "PING":
                    self.send("PONG :{0}".format(" ".join(event.arguments)))
                func_name = "on_"+event.text_type.lower()
                if hasattr(self, func_name):
                    getattr(self, func_name)(event)
                if hasattr(self, "on_all"):
                    self.on_all(event)
    #Basic client use
    def privmsg(self, channel, message):
        MSGLEN = 449 - len(channel)
        message_byte_count = sys.getsizeof(message)-37
        strings = [message[i:i+MSGLEN] for i in range(0, message_byte_count, MSGLEN)]
        for message in strings:
            self.send("PRIVMSG {0} :{1}".format(channel, message))
    def reply(self, event, message):
        self.privmsg(event.target, message)