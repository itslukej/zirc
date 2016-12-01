class Caps(object):
    def __init__(self, *args):
        self.caps = list(args)
        self.availablecaps = []
        self.stringcaps = []
        self.done = False
        self.args = {}
        for cap in self.caps:
            if not isinstance(cap, str):
                self.stringcaps.append(cap.name)
            else:
                self.stringcaps.append(cap)

    def handler(self, event):
        if event.arguments[0] == "LS" and not self.done:
            servcaps = event.arguments[1].split(' ')
            for c in servcaps:
                cap = c.split("=")[0]
                if cap in self.stringcaps:
                    self.availablecaps.append(cap)
                    if c.find('=') != -1:
                        args = c.split('=')[1]
                        self.args[cap] = args.split(',')
                    else:
                        self.args[cap] = None
                if not self.availablecaps:
                    self.bot.send("CAP END")
                else:
                    self.bot.send("CAP REQ :" + " ".join(self.availablecaps))
        elif event.arguments[0] == "ACK" and not self.done:
            for cap in self.caps:
                if hasattr(cap, "run"):
                    cap.run(self.bot, args=self.args[cap])
                self.done = True

    def run(self, bot):
        self.bot = bot
        self.bot.listen(self.handler, "cap")
        self.bot.send("CAP LS")

    __call__ = run
