from string import Template
from .flood import floodProtect
from .loop import EventLoop
from .errors import NoSocket, NoConfig
from . import util
from .wrappers import connection_wrapper

class Client(object):
    listeners = []

    def connect(self, config_class=None, keyfile=None, certfile=None):

        self.fp = floodProtect()
        if not hasattr(self, "connection"):
            raise NoSocket("{0} has no attribute 'connection'".format(self))
        if config_class is None:
            raise NoConfig("config_class not a argument when calling connect")

        self._config = config_class
        self.socket = self.connection((self._config["host"], self._config["port"]), keyfile=keyfile, certfile=certfile)

        self._config["caps"](self)

        if self._config.get("password"):
            self.send("PASS {0}".format(self._config["password"]))

        self.send("NICK {0}".format(self._config["nickname"]))
        self.send("USER {0} * * :{1}".format(self._config["ident"], self._config["realname"]))

        self._channels = self._config["channels"]
        self.loop = EventLoop(self.recv)

    def recv(self):
        self.buffer = ""
        while not self.buffer.endswith("\r\n"):
            self.buffer += self.socket.recv(2048).decode("utf-8", errors="replace")
        self.buffer = self.buffer.strip().split("\r\n")
        return self.buffer

    def send(self, data):
        if hasattr(self, "on_send"):
            self.on_send(data)
        self.fp.queue_add(self.socket, "{0}\r\n".format(data).encode("UTF-8"))

    def start(self):
        self.loop.create_job("main", self.main_job)
        self.loop.run()

    def main_job(self, event):
        """loop job to provide a event based system for clients."""
        args = {"event": event, "bot": self, "irc": connection_wrapper(self), "args": " ".join(event.arguments).split(" ")[1:]}

        # add arguments from event, for easier access
        args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})

        if event.type == "001":
            for channel in self._channels:
                self.send("JOIN {0}".format(channel))

        to_call = []

        if hasattr(self, "on_all"):
            to_call.append(self.on_all)

        if hasattr(self, "on_" + event.type.lower()):
            to_call.append(getattr(self, "on_" + event.type.lower()))

        if event.type != event.text_type:
            if hasattr(self, "on_" + event.text_type.lower()):
                to_call.append(getattr(self, "on_" + event.text_type.lower()))

        for event_name, func in self.listeners:
            if event_name == event.text_type.lower() or event_name == event.type.lower():
                to_call.append(func)
        # Call the functions here
        for call_func in to_call:
            util.function_argument_call(call_func, args)()

        if event.type == "PING":
            self.send("PONG :{0}".format(" ".join(event.arguments)))

        # CTCP Replies
        if event.type == "PRIVMSG" and " ".join(event.arguments).startswith("\x01") and hasattr(self, "ctcp"):
            ctcp_message = " ".join(event.arguments).replace("\x01", "").upper()
            if ctcp_message in self.ctcp.keys():
                if callable(self.ctcp[ctcp_message]):
                    result = self.ctcp[ctcp_message]()
                else:
                    result = self.ctcp[ctcp_message]
                self.send("NOTICE {0} :{1} {2}".format(event.source.nick, ctcp_message, result))

        if event.type == "332":
            self.userdb[event.target]["topic"] = " ".join(event.arguments)

    # Basic client use
    def privmsg(self, channel, message, background=None, rainbow=False, style=None):
        MSGLEN = 400 - len("PRIVMSG {} :\r\n".format(channel).encode())
        strings = [message[i:i + MSGLEN] for i in range(0, len(message), MSGLEN)]
        for message in strings:
            msg = Template(message).safe_substitute(**util.colors.colors)
            if rainbow:
                msg = util.colors.rainbow(msg)
            self.send("PRIVMSG {0} :{1}".format(channel, util.colors.stylize(util.colors.background(msg, background), style)))

    def reply(self, event, message, background=None, rainbow=False, style=None):
        if event.target == self._config['nickname']:
            self.privmsg(event.source.nick, message, background=background, rainbow=rainbow, style=style)
        else:
            self.privmsg(event.target, message, background=background, rainbow=rainbow, style=style)

    def listen(self, func, event_name):
        self.listeners.append((event_name.lower(), func))
