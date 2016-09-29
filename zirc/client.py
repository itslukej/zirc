from .event import Event
from . import util

import asyncio, socket

class Client(object):
    def __init__(self, loop=None):
        self.listeners = []
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.buffer = asyncio.Queue()
        self.loop.create_task(self.buffer_handler())

    def connect(self, config_class = None):

        if not hasattr(self, "connection"):
            raise NoSocket("{0} has no attribute 'connection'".format(self))
        if config_class is None:
            raise NoConfig("config_class not a argument when calling connect")
        
        self._config = config_class

        self.loop.run_until_complete(self._connect())
        self.loop.run_forever()
        #self._config["caps"](self)

    async def _connect(self):
        #start socket
        self.reader, self.writer = await self.connection(self.loop, (self._config["host"], self._config["port"]))

        if self._config.get("password"):
            await self.send("PASS {0}".format(self._config["password"]))

        await self.send("NICK {0}".format(self._config["nickname"]))
        await self.send("USER {0} * * :{1}".format(self._config["ident"], self._config["realname"]))

        self._channels = self._config["channels"]

        self.loop.create_task(self.main())

    async def main(self):
        while True:
            recv = await self.recv()
            for line in recv:
                event = Event(line)
                
                args = {"event": event, "bot": self, "args": " ".join(event.arguments).split(" ")[1:]}
                args.update({k: getattr(event, k) for k in dir(event) if not k.startswith("__") and not k.endswith("__")})

                if event.type == "001":
                    for channel in self._channels:
                        await self.join(channel)

                to_call = []

                if hasattr(self, "on_all"):
                    to_call.append(self.on_all)

                if hasattr(self, "on_"+event.type.lower()):
                    to_call.append(getattr(self, "on_"+event.type.lower()))
                
                if event.type != event.text_type:
                    if hasattr(self, "on_"+event.text_type.lower()):
                        to_call.append(getattr(self, "on_"+event.text_type.lower()))

                for event_name, func in self.listeners:
                    if event_name == event.text_type.lower() or event_name == event.type.lower():
                        to_call.append(func)

                for call_func in to_call:
                    func = util.function_argument_call(call_func, args)
                    await func()

                if event.type == "PING":
                    self.send("PONG :{0}".format(" ".join(event.arguments)))


    async def recv(self):
        raw = ""
        while not raw.endswith("\r\n"):
            recvd = await self.reader.read(2048)
            raw += recvd.decode("utf-8", errors="replace")
        raw = raw.strip().split("\r\n")
        return raw

    async def send(self, data):
        await self.buffer.put("{0}\r\n".format(data).encode("UTF-8"))
        if hasattr(self, "on_send"):
            await self.on_send(data)

    async def buffer_handler(self):
        while True:
            raw = await self.buffer.get()
            self.writer.write(raw)
            await asyncio.sleep(1)

    async def privmsg(self, channel, message):
        await self.send("PRIVMSG {0} :{1}".format(channel, message))

    msg = privmsg

    async def reply(self, event, message):
        await self.privmsg(event.target, message)

    async def ping(self):
        await self.send("PING :{}".format(str(int(time()))).encode('utf-8'))

    async def part(self, chan):
        await self.send("PART {0}".format(chan))

    async def nick(self, nick):
        await self.send("NICK {0}".format(nick))

    async def join(self, chan):
        await self.send("JOIN {0}".format(chan))

    async def invite(self, chan, user):
        await self.send("INVITE {0} {1}".format(user, chan))

    async def action(self, channel, message):
        self.sendmsg(channel,"\x01ACTION " + message + "\x01")

    async def kick(self,channel, user, message):
        user = user.replace(" ","").replace(":","")
        await self.send("KICK " + channel + " " + user+ " :" + message)

    async def op(self, channel, nick):
        await self.send("MODE {0} +o {1}".format(channel, nick))

    async def deop(self, channel, nick):
        await self.send("MODE {0} -o {1}".format(channel, nick))

    async def ban(self, channel, nick):
        await self.send("MODE {0} +b {1}".format(channel, nick))

    async def unban(self, channel, nick):
        await self.send("MODE {0} -b {1}".format(channel, nick))

    async def quiet(self, channel, nick):
        await self.send("MODE {0} +q {1}".format(channel, nick))

    async def unquiet(self, channel, nick):
        await self.send("MODE {0} -q {1}".format(channel, nick))

    async def unvoice(self, channel, nick):
        await self.send("MODE {0} -v {1}".format(channel, nick))

    async def voice(self, channel, nick):
        await self.send("MODE {0} +v {1}".format(channel, nick))

    async def mode(self, channel, nick, mode):
        await self.send("MODE {0} {1} {2}".format(channel, mode, nick))
        
    async def notice(self, user, message):
        await self.send("NOTICE {0} :{1}".format(user, message))

    async def quit(self, message=""):
        await self.send("QUIT :"+message)
    
    async def ctcp(self, user, message):
        await self.send("PRIVMSG {0} :\x01{1}\x01\x01".format(user, message))
