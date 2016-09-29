import socket, asyncio

class Socket(object):
    """
    A class for creating socket connections.
    
    Creating a connection:
        address = ("irc.stuxnet.xyz", 6697)
        Socket(ssl=True, family=socket.AF_INET6)(address)
    """
    def __init__(self, family=socket.AF_INET, ssl=False):
        self.family = family
        self.ssl = ssl
    async def connect(self, loop, address):
        host = address[0]
        port = address[1]

        socket = await asyncio.open_connection(host=host, port=port, loop=loop, family=self.family, ssl=self.ssl)
        return socket
    __call__ = connect