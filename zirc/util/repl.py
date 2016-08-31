import code, sys

class Repl(code.InteractiveConsole):
    '''Interractive Python Console class'''
    def __init__(self, items=None):
        if items is None:
            items = {}
        code.InteractiveConsole.__init__(self, items)
        self._buffer = ""

    def write(self, data):
        self._buffer += str(data)

    def run(self, data):
        sys.stdout = self
        self.push(data)
        sys.stdout = sys.__stdout__
        result = self._buffer
        self._buffer = ""
        return result

    def showtraceback(self):
        exc_type, value, lasttb = sys.exc_info()
        self._buffer+="{0}: {1}".format(exc_type.__name__, value)

    def showsyntaxerror(self, *args):
        self.showtraceback()
