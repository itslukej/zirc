from .event import Event
from .wrappers import connection_wrapper
from . import errors, util

class TestCase(object):
    def start(self, log):
        print("Starting...")
        log = log.split("\n")
        for line in log:
            try:
                event = Event(line)
                print("Parsed line '{0}'".format(line))
            except:
                raise errors.InvalidLine(line)

            args = {"event": event, "bot": self, "irc": connection_wrapper(self), "args": " ".join(event.arguments).split(" ")[1:]}
            args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})

            if hasattr(self, "on_all"):
                print("Attempting to run on_all...")
                util.function_argument_call(self.on_all, args)()

            text_type_func_name = "on_" + event.text_type.lower()
            if hasattr(self, text_type_func_name):
                print("Attempting to run {0}".format(text_type_func_name))
                util.function_argument_call(getattr(self, text_type_func_name), args)()

            raw_type_func_name = "on_" + event.type.lower()
            if raw_type_func_name != text_type_func_name:
                if hasattr(self, raw_type_func_name):
                    print("Attempting to run {0}".format(raw_type_func_name))
                    util.function_argument_call(getattr(self, raw_type_func_name), args)()
 
            if event.type == "PING":
                self.send("PONG :{0}".format(" ".join(event.arguments)))
        print("Done!")

    def send(self, data):
        print("RESPONSE: '{0}'".format(data))
        if hasattr(self, "on_send"):
            self.on_send(data)

    def reply(self, event, message):
        if event.target == 'zIRC-test':
            self.privmsg(event.source.nick, message)
        else:
            self.privmsg(event.target, message)

    def privmsg(self, channel, message):
        self.send("PRIVMSG {0} :{1}".format(channel, message))
