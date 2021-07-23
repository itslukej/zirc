import code, sys
from typing import Any, AnyStr, Mapping, Optional

class Repl(code.InteractiveConsole):
    """Interractive Python Console class"""
    def __init__(self, items: Optional[Mapping[str, Any]]=None):
        if items is None:
            items = {}
        code.InteractiveConsole.__init__(self, items)
        self._buffer = ""

    def write(self, data: AnyStr):
        self._buffer += str(data)

    def flush(self):
        self._buffer = ""

    def run(self, data: str):
        sys.stdout = self
        self.push(data)
        sys.stdout = sys.__stdout__
        result = self._buffer
        self._buffer = ""
        return result

    def showtraceback(self):
        exc_type, value, lasttb = sys.exc_info()
        self._buffer += "{0}: {1}".format(exc_type.__name__, value)

    def showsyntaxerror(self, *args):
        self.showtraceback()
