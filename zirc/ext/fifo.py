import os, threading

def fifo_while(send_function, name):
    if not os.path.exists(name):
        os.mkfifo(name)
    with open(name, "r") as file:
        while True:
            line = file.readline()[:-1]
            if len(line) > 0:
                send_function(line)
                
def Fifo(send_function, name="fifo"):
    thread = threading.Thread(target=fifo_while, args=(send_function, name))
    thread.daemon = True
    thread.start()