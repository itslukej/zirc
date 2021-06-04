from threading import Thread
from time import sleep

class floodProtect(object):

    def __init__(self):
        self.irc_queue = []
        self.irc_queue_running = False
        self.sleep_time = 1
        self.lines = 1
        self.canburst = True

    def queue_thread(self):
        burstdone = False
        while True:
            if len(self.irc_queue):
                if not burstdone:
                    for item in self.irc_queue[:self.lines]:
                        try:
                            connection, raw = item
                        except Exception:
                            self.irc_queue_running = False
                            break
                        connection.send(raw)
                        self.irc_queue.remove(item)
                    burstdone = True
                if len(self.irc_queue) == 0:
                    burstdone = False
                else:
                    try:
                        connection, raw = self.irc_queue.pop(0)
                    except Exception:
                        self.irc_queue_running = False
                        break
                    connection.send(raw)
                    sleep(self.sleep_time)
            else:
                burstdone = False
            sleep(0.2)


    def queue_add(self, connection, raw):
        self.irc_queue.append([connection, raw])
        if getattr(self, 'queuet', None) is None:
            self.irc_queue_running = True
            self.queuet = Thread(target=self.queue_thread)
            self.queuet.daemon = True
            self.queuet.start()

    def queue_add_first(self, connection, raw):
        self.irc_queue = [[connection, raw]] + self.irc_queue
        if getattr(self, 'queuet', None) is None:
            self.irc_queue_running = True
            self.queuet = Thread(target=self.queue_thread)
            self.queuet.daemon = True
            self.queuet.start()
