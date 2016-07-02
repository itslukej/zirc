from threading import Thread
from time import sleep

class floodProtect(object):

    def __init__(self):
        self.irc_queue = []
        self.irc_queue_running = False

    def queue_thread(self):
        while True:
            try:
                connection = self.irc_queue[0][0]
                raw = self.irc_queue[0][1]
                self.irc_queue.pop(0)
            except:
                self.irc_queue_running = False
                break
            connection.send(raw)
            sleep(1)

    def queue_add(self, connection, raw):
        self.irc_queue.append([connection, raw])
        if not self.irc_queue_running:
            self.irc_queue_running = True
            self.queuet = Thread(target=self.queue_thread)
            self.queuet.daemon = True
            self.queuet.start()

    def queue_add_first(self, connection, raw):
        self.irc_queue=[[connection,raw]]+self.irc_queue
        if not self.irc_queue_running:
            self.irc_queue_running = True
            self.queuet = Thread(target=self.queue_thread)
            self.queuet.daemon = True
            self.queuet.start()