from .connection import Socket
from .event import Event
from .flood import floodProtect
from .loop import EventLoop
from .errors import *
from . import util
from .wrappers import connection_wrapper

from base64 import b64encode
import sys,time

class Client(object):
    def connect(self, config_class = None):

        self.fp = floodProtect()
        if not hasattr(self, "connection"):
            raise NoSocket("{0} has no attribute 'connection'".format(self))
        if config_class is None:
            raise NoConfig("config_class not a argument when calling connect")
            
        self._config = config_class
        self.socket = self.connection((self._config["host"], self._config["port"]))

        if self._config["sasl_user"] is not None and self._config["sasl_pass"] is not None:
            self.do_sasl(self._config["sasl_user"], self._config["sasl_pass"])

        self.send("NICK {0}".format(self._config["nickname"]))
        self.send("USER {0} * * :{1}".format(self._config["ident"], self._config["realname"]))
        
        self._channels = self._config["channels"]
    def recv(self):
        self.buffer= ""
        while not self.buffer.endswith("\r\n"):
            self.buffer += self.socket.recv(2048).decode("utf-8", errors="replace")
        self.buffer = self.buffer.strip().split("\r\n")
        return self.buffer
    def send(self, data):
        if hasattr(self, "on_send"):
            self.on_send(data)
        self.fp.queue_add(self.socket, "{0}\r\n".format(data).encode("UTF-8"))
    def start(self):
        self.loop = EventLoop(self.recv)
        self.loop.create_job("main", self.main_job)
        self.loop.run()
    def main_job(self, event):
        """loop job to provide a event based system for clients."""
        args = {"event": event, "bot": self, "irc": connection_wrapper(self)}
        
        #add arguments from event, for easier access
        args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})
    
        if event.type == "001":
            for channel in self._channels:
                self.send("JOIN {0}".format(channel))
    
        if hasattr(self, "on_all"):
            util.function_argument_call(self.on_all, args)()
    
        #e.g on_welcome
        text_type_func_name = "on_"+event.text_type.lower()
        if hasattr(self, text_type_func_name):
            util.function_argument_call(getattr(self, text_type_func_name), args)()
    
        #e.g on_001
        raw_type_func_name = "on_"+event.type.lower()
        if raw_type_func_name != text_type_func_name:
            if hasattr(self, raw_type_func_name):
                util.function_argument_call(getattr(self, raw_type_func_name), args)()
    
        if event.type == "PING":
            self.send("PONG :{0}".format(" ".join(event.arguments)))
    
        #CTCP Replies
        if event.type == "PRIVMSG" and " ".join(event.arguments).startswith("\x01") and hasattr(self, "ctcp"):
            ctcp_message = " ".join(event.arguments).replace("\x01", "").upper()
            if ctcp_message in self.ctcp.keys():
                if callable(self.ctcp[ctcp_message]):
                    result = self.ctcp[ctcp_message]()
                else:
                    result = self.ctcp[ctcp_message]
                self.send("NOTICE {0} :{1} {2}".format(event.source.nick, ctcp_message, result))
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
    def do_sasl(self, user, passw):
        self.send("CAP REQ :sasl")
        while True:
            for line in self.recv():
                line = line.split()
                if line[0] == "AUTHENTICATE":
                    if line[1] == "+":
                        saslstring = b64encode("{0}\x00{0}\x00{1}".format(
                                        user,
                                        passw).encode("UTF-8"))
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
