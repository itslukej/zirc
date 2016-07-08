from .connection import Socket
from .event import Event
from .flood import floodProtect
from base64 import b64encode

from .errors import *
from . import util

import sys,time

class NoSocket(Exception):
    pass

class Client(object):
    def connect(self, address, port, nickname, ident, realname, channels, sasl_user=None, sasl_pass=None):
        self.channels = channels
        
        self.fp = floodProtect()
        if not hasattr(self, "connection"):
            raise NoSocket("{0} has no attribute 'connection'".format(self))
        self.socket = self.connection((address, port))
        if sasl_pass is not None and sasl_user is not None:
            self.sasl_user = sasl_user
            self.sasl_pass = sasl_pass
            self.do_sasl()
        self.send("NICK {0}".format(nickname))
        self.send("USER {0} * * :{1}".format(ident, realname))
    def recv(self):
        self.part = ""
        self.data = ""
        while not self.part.endswith("\r\n"):
            self.part = self.socket.recv(2048).decode("utf-8", errors="replace")
            self.data += self.part
        self.data = self.data.strip().split("\r\n")
        return self.data
    def send(self, data):
        if hasattr(self, "on_send"):
            self.on_send(data)
        self.fp.queue_add(self.socket, "{0}\r\n".format(data).encode("UTF-8"))
    def start(self):
        while True:
            for query in self.recv():
                event = Event(query)
                args = {"event": event, "irc": self}
                
                #add arguments from event, for easier access
                args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})

                if event.type == "PING":
                    self.send("PONG :{0}".format(" ".join(event.arguments)))
                if event.type == "001":
                    for channel in self.channels:
                        self.send("JOIN {0}".format(channel))

                if hasattr(self, "on_all"):
                    util.function_argument_call(self.on_all, args)()

                text_type_func_name = "on_"+event.text_type.lower()
                if hasattr(self, text_type_func_name):
                    util.function_argument_call(getattr(self, text_type_func_name), args)()

                raw_type_func_name = "on_"+event.type.lower()
                if raw_type_func_name != text_type_func_name:
                    if hasattr(self, raw_type_func_name):
                        util.function_argument_call(getattr(self, raw_type_func_name), args)()
    #Basic client use
    def privmsg(self, channel, message):
        MSGLEN = 449 - len(channel)
        message_byte_count = sys.getsizeof(message)-37
        strings = [message[i:i+MSGLEN] for i in range(0, message_byte_count, MSGLEN)]
        for message in strings:
            self.send("PRIVMSG {0} :{1}".format(channel, message))
    def reply(self, event, message):
        self.privmsg(event.target, message)
    #SASL Auth
    def do_sasl(self):
        self.send("CAP REQ :sasl")
        while True:
            for line in self.recv():
                line = line.split()
                if line[0] == "AUTHENTICATE":
                    if line[1] == "+":
                        saslstring = b64encode("{0}\x00{0}\x00{1}".format(
                                        self.sasl_user,
                                        self.sasl_pass).encode("UTF-8"))
                        self.send("AUTHENTICATE {0}".format(saslstring.decode("UTF-8")))
                elif line[1] == "CAP":
                    if line[3] == "ACK":
                        line[4] = line[4].strip(":")
                        caps = line[4:]
                        if "sasl" in caps:
                            self.send("AUTHENTICATE PLAIN")
                elif line[1] == "903":
                    self.send("CAP END")
                    return True
                elif line[1] == "904" or line[1] == "905" or line[1] == "906":
                    error = " ".join(line[2:]).strip(":")
                    self.send("QUIT :[ERROR] {0}".format(error))
                    raise SASLError(error)