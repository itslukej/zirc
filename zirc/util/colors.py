colors = {
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

def getcolor(color):
    for key in colors.keys():
        if color in colors[key]:
            return key
        else:
            pass

def color(string, c):
    if c == 'rainbow':
        i = 0
        colored = ""

        for character in string:
            if i > (len(rainbow) - 1):  # We substract one because i starts at 0 and len(rainbow) at 1
                i = 0

            colored += "\x03{0}{1}".format(getcolor(rainbow[i]), character)
            i += 1

        return colored + "\x0F"
    elif c is None:
        return string
    else:
        return "\x03{}{}\x0F".format(getcolor(c), string)   
