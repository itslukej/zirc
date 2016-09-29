import zirc, asyncio, sys, os

class Bot(zirc.Client):
    def __init__(self):
        zirc.Client.__init__(self)
        self.connection = zirc.Socket()
        self.config = zirc.IRCConfig(host="irc.stuxnet.xyz", port=6667, nickname="zIRC-CI-"+str(sys.version.split(" ")[0].replace(".", "-").replace("+", "")), ident="ci", realname="zIRC IRCP Library", channels=[])
        self.connect(self.config)

    async def on_welcome(self, event):
        await self.send("JOIN #zirc")
        await asyncio.sleep(1)
        await self.privmsg("#zirc", "Testing script successful")
        await asyncio.sleep(1)
        await self.send("QUIT :My work here is done")
        await asyncio.sleep(1)
        os._exit(0)

    async def on_all(irc, event):
        print(event)

Bot()
