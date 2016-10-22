colours = {
    '00': ['white'],
    '01': ['black'],
    '02': ['navy'],
    '03': ['green'],
    '04': ['red'],
    '05': ['brown', 'maroon'],
    '06': ['purple', 'violet'],
    '07': ['olive'],
    '08': ['yellow'],
    '09': ['lightgreen', 'lime'],
    '10': ['teal', 'bluecyan'],
    '11': ['cyan', 'aqua'],
    '12': ['blue', 'royal'],
    '13': ['pink', 'lightpurple', 'fuchsia'],
    '14': ['gray', 'grey'],
    '15': ['lightgray', 'lightgrey', 'silver'],
}
rainbow = ['red', 'olive', 'yellow', 'green', 'blue', 'navy', 'violet']

def getColour(colour):
    for key in colours.keys():
        if colour in colours[key]:
            return key
        else:
            pass

def colour(string, c):
    if c == 'rainbow':
        rainbow(string)
    elif c is None:
        return string
    else:
        return "\x03{}{}\x0F".format(getColour(c), string)

def rainbow(string):
    i = 0
    coloured = ""

    for character in string:
        if i > (len(rainbow) - 1):  # We substract one because i starts at 0 and len(rainbow) at 1
            i = 0

        coloured += "\x03{0}{1}".format(getColour(rainbow[i]), character)
        i += 1

    return returned + "\x0F"
