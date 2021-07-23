from typing import Optional
from .event import Event
from .wrappers import connection_wrapper
from . import errors, util

class TestCase(object):
    def start(self, log: str):
        print("Starting...\n", flush=True)
        log = log.split("\n")
        for line in log:
            try:
                event = Event(line)
                print("Parsed line '{0}'".format(line), flush=True)
            except Exception:
                raise errors.InvalidLine(line)

            args = {"event": event, "bot": self, "irc": connection_wrapper(self), "args": " ".join(event.arguments).split(" ")[1:]}
            args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})

            if hasattr(self, "on_all"):
                print("Attempting to run on_all...", flush=True)
                util.function_argument_call(self.on_all, args)()

            text_type_func_name = "on_" + event.text_type.lower()
            if hasattr(self, text_type_func_name):
                print("Attempting to run {0}".format(text_type_func_name), flush=True)
                util.function_argument_call(getattr(self, text_type_func_name), args)()

            raw_type_func_name = "on_" + event.type.lower()
            if raw_type_func_name != text_type_func_name:
                if hasattr(self, raw_type_func_name):
                    print("Attempting to run {0}".format(raw_type_func_name), flush=True)
                    util.function_argument_call(getattr(self, raw_type_func_name), args)()

            if event.type == "PING":
                self.send("PONG :{0}".format(" ".join(event.arguments)))
        print("Done!", flush=True)

    def send(self, data: str):
        print("RESPONSE: '{0}'\n".format(data), flush=True)
        if hasattr(self, "on_send"):
            self.on_send(data)

    def reply(self, event: Event, message: str, background: Optional[str]=None, rainbow: Optional[bool]=False, style: Optional[str]=None):
        if event.target == 'zIRC-test':
            self.privmsg(event.source.nick, message, background=background, rainbow=rainbow, style=style)
        else:
            self.privmsg(event.target, message, background=background, rainbow=rainbow, style=style)

    def privmsg(self, channel: str, message: str, background: Optional[str]=None, rainbow: Optional[bool]=False, style: Optional[str]=None):
        del background
        del rainbow
        del style
        self.send("PRIVMSG {0} :{1}".format(channel, message))
