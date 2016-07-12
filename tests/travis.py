import zirc, ssl, time, sys, os

class Bot(zirc.Client):
    def __init__(self):
        self.connection = zirc.Socket(wrapper=ssl.wrap_socket)
        self.config = zirc.IRCConfig(host="irc.stuxnet.xyz", port=6697, nickname="zIRC-CI-"+str(sys.version.split(" ")[0].replace(".", "-").replace("+", "")), ident="ci", realname="zIRC IRCP Library", channels=[])
        self.connect(self.config)
        self.start()

    def on_welcome(irc, event):
        irc.send("JOIN #zirc")
        time.sleep(1)
        irc.privmsg("#zirc", "Testing script successful")
        time.sleep(1)
        irc.send("QUIT :My work here is done")
        time.sleep(1)
        os._exit(0)

    def on_all(irc, event):
        print(event)

Bot()
