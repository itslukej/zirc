import zirc, time, sys, os

class Bot(zirc.Client):
    def __init__(self):
        self.connection = zirc.Socket()
        self.config = zirc.IRCConfig(host="irc.freenode.net", port=6667, nickname="zIRC-CI-"+str(sys.version.split(" ")[0].replace(".", "-").replace("+", "")), ident="ci", realname="zIRC IRCP Library", channels=["##zirc-invalid"], caps=zirc.Caps(zirc.Sasl(username="zIRC", password=os.environ['irc_pass'])))
        self.connect(self.config)
        self.start()

    @staticmethod
    def on_join(irc, event):
        irc.notice("#zirc", "Testing script successful")
        time.sleep(1)
        irc.send("QUIT :My work here is done")
        time.sleep(1)
        os._exit(0)

    @staticmethod
    def on_all(irc, event):
        print(event)

    def on_nicknameinuse(self, irc, event):
        irc.nick(self.config['nickname'] + '_')

Bot()
