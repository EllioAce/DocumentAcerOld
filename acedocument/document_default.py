"""A container for the defaults of a document acer document"""
import ast

defaultTextSize = 16
defaultFont = "CascadiaCode.ttf"
defaultXPosition = 0
defaultYPosition = 0
defaultImageWidth = 1000
defaultImageHeight = 1000
defaultLineSize = 10
defaultAnchor = "LEFT"
defaultColumnHeight = 200
defaultColumnWidth = 400


def __init__(file):
    """Collect all defaults listed within the document"""
    global defaultTextSize
    global defaultFont
    global defaultXPosition
    global defaultYPosition
    global defaultImageWidth
    global defaultImageHeight
    global defaultLineSize
    global defaultAnchor
    global defaultColumnHeight
    global defaultColumnWidth
    for line in file:
        if line == "DEFAULTS_START":
            continue
        elif line == "DEFAULTS_END":
            break
        defaultTextSize = declare_value_type(find_default_in_line(line, "DefaultSize", defaultTextSize))
        defaultFont = find_default_in_line(line, "DefaultFont", defaultFont)
        defaultXPosition = declare_value_type(find_default_in_line(line, "DefaultX", defaultXPosition))
        defaultYPosition = declare_value_type(find_default_in_line(line, "DefaultY", defaultYPosition))
        defaultImageWidth = declare_value_type(find_default_in_line(line, "DefaultImageWidth", defaultImageWidth))
        defaultImageHeight = declare_value_type(find_default_in_line(line, "DefaultImageHeight", defaultImageHeight))
        defaultLineSize = declare_value_type(find_default_in_line(line, "DefaultLineWidth", defaultLineSize))
        defaultAnchor = find_default_in_line(line, "DefaultAnchor", defaultAnchor)
        defaultColumnHeight = declare_value_type(find_default_in_line(line, "DefaultColumnHeight", defaultColumnHeight))
        defaultColumnWidth = declare_value_type(find_default_in_line(line, "DefaultColumnWidth", defaultColumnWidth))


def find_default_in_line(line: str, valuename: str, defaultvalue="0"):
    """Find any listed default in the line provided"""
    if line.__contains__(f'{valuename}='):
        print(line.replace(f'{valuename}=', '').replace('\n', ''))
        return line.replace(f'{valuename}=', '').replace('\n', '')
    return str(defaultvalue)


def declare_value_type(value: str):
    """Returns the same value, but with a type other than string"""
    return ast.literal_eval(value)
