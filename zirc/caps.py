class Caps(object):
    def __init__(self, *args):
        self.caps = list(args)
        self.availablecaps = []
        self.stringcaps = []
        self.done = False
        for cap in self.caps:
            if not isinstance(cap, str):
                self.stringcaps.append(cap.name)
            else:
                self.stringcaps.append(cap)

    def handler(self, event):
        if not self.done:
            if event.arguments[0] == "LS":
                servcaps = event.arguments[1].split(' ')
                for c in servcaps:
                    if c in self.stringcaps:
                        self.availablecaps.append(c)
                if not self.availablecaps:
                    self.bot.send("CAP END")
                else:
                    self.bot.send("CAP REQ :" + " ".join(self.availablecaps))
                self.done = True
            elif event.arguments[0] == "ACK":
                for cap in self.caps:
                    if hasattr(cap, "run"):
                        cap.run(self.bot)
                self.done = True

    def run(self, bot):
        self.bot = bot
        self.bot.listen(self.handler, "cap")
        self.bot.send("CAP LS")

    __call__ = run
