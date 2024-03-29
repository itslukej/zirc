colors = {
    "WHITE": "\x0300",
    "BLACK": "\x0301",
    "NAVY": "\x0302",
    "GREEN": "\x0303",
    "RED": "\x0304",
    "BROWN": "\x0305",
    "MAROON": "\x0305",
    "PURPLE": "\x0306",
    "VIOLET": "\x0306",
    "ORANGE": "\x0307",
    "YELLOW": "\x0308",
    "LIGHTGREEN": "\x0309",
    "LIME": "\x0309",
    "TEAL": "\x0310",
    "BLUECYAN": "\x0310",
    "CYAN": "\x0311",
    "AQUA": "\x0311",
    "BLUE": "\x0312",
    "ROYAL": "\x0312",
    "LIGHTPURPLE": "\x0313",
    "PINK": "\x0313",
    "FUCHSIA": "\x0313",
    "GREY": "\x0314",
    "GRAY": "\x0314",
    "LIGHTGRAY": "\x0315",
    "LIGHTGREY": "\x0315",
    "SILVER": "\x0315",

    "NORMAL": "\x0F",
    "UNDERLINE": "\x1F",
    "BOLD": "\x02",
    "ITALIC": "\x1D",
    "REVERSE": "\u202E"
}

_rainbow = ["red", "orange", "yellow", "green", "blue", "navy", "violet"]


def rainbow(string: str):
    i = 0
    colored = ""

    for character in string:
        if i > (len(_rainbow) - 1):  # We substract one because i starts at 0 and len(rainbow) at 1
            i = 0

        colored += "{0}{1}".format(colors[_rainbow[i].upper()], character)
        i += 1

    return colored + "\x0F"

def background(string: str, bg: str):
    c = string.find("\x03") != -1
    if c and bg is not None:
        return "{0},{1}{2}".format(string[:3], colors[bg][1:], string[3:])
    elif not c and bg is not None:
        return "{0},{1}{2}\x0F".format(colors["black"], colors[bg][1:], string)
    elif bg is None:
        return string

def stylize(string: str, style: str):
    if style is not None:
        return "{0}{1}".format(colors[style.upper()], string)
    else:
        return string
