import socks,socket
SOCKS5 = socks.SOCKS5
SOCKS4 = socks.SOCKS4
HTTP = socks.HTTP

class Proxy(socks.socksocket):
    def __init__(self, host="localhost", port=1080, protocol=socks.SOCKS5, family=socket.AF_INET, type=socket.SOCK_STREAM):
        socks.socksocket.__init__(self, family, type)
        self.set_proxy(protocol, host, port)
        
        self.host = host
        self.port = port
        self.protocol = protocol
    def __repr__(self):
        return "Proxy({0}, {1})".format(self.host, self.protocol)