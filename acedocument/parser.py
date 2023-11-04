"""Parses a document acer program into instructions for the program to execute"""
from acedocument.instruction import *
from acedocument import document_default


def parseline(line: str):
    """Parse a line into an instruction for the program to execute"""
    instructionline = line.replace('\n', '')
    if instructionline == 'CREATENEWPAGE':
        return NewPageInstruction()
    elif instructionline.__contains__('IMAGE->'):
        imageinstruction, parametersign, parameters = instructionline.partition('::')
        imagesign, directorysign, directory = imageinstruction.partition('->')
        x = propertytoint(findproperty("X", parameters), document_default.defaultXPosition)
        y = propertytoint(findproperty("Y", parameters), document_default.defaultYPosition)
        width = propertytoint(findproperty("Width", parameters), document_default.defaultImageWidth)
        height = propertytoint(findproperty("Height", parameters), document_default.defaultImageHeight)
        return ImageInstruction(directory, x, y, width, height)
    elif instructionline.__contains__('LINE->'):
        lineinstruction, parametersign, parameters = instructionline.partition('::')
        linesign, ysign, y = lineinstruction.partition('->')
        y = propertytoint(y, document_default.defaultYPosition)
        size = propertytoint(findproperty("Size", parameters), document_default.defaultLineSize)
        return LineInstruction(y, size)
    elif instructionline.__contains__('TABLE->'):
        lineinstruction, parametersign, parameters = instructionline.partition('::')
        tablesign, sectionsign, sectionline = lineinstruction.partition('->')
        column_width = propertytoint(findproperty("ColumnWidth", parameters), document_default.defaultColumnWidth)
        column_height = propertytoint(findproperty("ColumnHeight", parameters), document_default.defaultColumnHeight)
        font_size = propertytoint(findproperty("TextSize", parameters), document_default.defaultTextSize)
        x = propertytoint(findproperty("X", parameters), document_default.defaultXPosition)
        y = propertytoint(findproperty("Y", parameters), document_default.defaultYPosition)
        font = findproperty("Font", parameters, document_default.defaultFont)
        texts: list[list[str]] = []
        sections: list[str] = sectionline.split(' ;; ')
        for section in sections:
            section_texts = section.split(' || ')
            texts.append(section_texts)
        return TableInstruction(font, x, y, font_size, column_width, column_height, texts)

    elif instructionline.__contains__('::'):
        text, parametersign, parameters = instructionline.partition('::')
        size = propertytoint(findproperty("Size", parameters), document_default.defaultTextSize)
        x = propertytoint(findproperty("X", parameters), document_default.defaultXPosition)
        y = propertytoint(findproperty("Y", parameters), document_default.defaultYPosition)
        font = findproperty("Font", parameters, document_default.defaultFont)
        anchor = findproperty("Anchor", parameters, document_default.defaultAnchor)
        fontname, dot, fileformat = font.partition('.')
        if parameters.__contains__("ITALICSBOLD") or parameters.__contains__("BOLDITALICS"):
            fontname = fontname.replace('-Regular', '')
            fontname += "-BoldItalic"
        elif parameters.__contains__("BOLD"):
            fontname = fontname.replace('-Regular', '')
            fontname += "-Bold"
        elif parameters.__contains__("ITALICS"):
            fontname = fontname.replace('-Regular', '')
            fontname += "-Italic"
        font = fontname + dot + fileformat
        return TextInstruction(font, text, size, x, y, anchor)

    return Instruction()


def findproperty(prop: str, propline: str, default: str = ""):
    """Finds a specific property within a list of properties"""
    if propline.__contains__(prop):
        propstr: str = ""
        index: int = 0
        propindex: int = propline.index(f"{prop}->")
        for char in propline:
            index += 1
            if index < propindex:
                continue
            if char == "," or char == ";":
                break
            propstr += char
        return propstr.replace(f" {prop}->", "")
    return default


def propertytoint(prop: str, default: int = 0):
    """Converts a property into an integer"""
    propint: int = default
    if prop == "":
        propint = default
    else:
        propint = int(prop)
    return propint
