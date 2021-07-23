import os, threading
from typing import Any, Callable

def fifo_while(send_function: Callable[[str], Any], name: str):
    if not os.path.exists(name):
        os.mkfifo(name)
    with open(name, "r") as f:
        while True:
            line = f.readline()[:-1]
            if len(line) > 0:
                send_function(line)

def Fifo(send_function: Callable[[str], Any], name: str="fifo"):
    thread = threading.Thread(target=fifo_while, args=(send_function, name))
    thread.daemon = True
    thread.start()
