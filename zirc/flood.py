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
        while True:
            self.canburst = True if len(self.irc_queue) == 0 else self.canburst
            if self.canburst:
                for i in range(0, self.lines):
                    try:
                        connection, raw = self.irc_queue.pop(0)
                    except Exception:
                        self.irc_queue_running = False
                        break
                    connection.send(raw)
                    sleep(self.sleep_time)
                sleep(0.1) # Sleep here so we have an extra little buffer and so we can flush the queue
                self.canburst = False
            else:
                try:
                    connection, raw = self.irc_queue.pop(0)
                except Exception:
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
        self.irc_queue = [[connection, raw]] + self.irc_queue
        if not self.irc_queue_running:
            self.irc_queue_running = True
            self.queuet = Thread(target=self.queue_thread)
            self.queuet.daemon = True
            self.queuet.start()
