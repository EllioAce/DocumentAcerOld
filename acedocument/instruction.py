"""Instructions for the program to execute"""
from acedocument.document_default import *


class Instruction:
    """An instruction for the program to execute"""
    def __init__(self):
        pass

    def __str__(self):
        return f'Raw Instruction, no parameters'


class TextInstruction(Instruction):
    """An instruction which tells the program to create text with parameters"""
    def __init__(self, font: str = defaultFont, text: str = "", size: int = defaultTextSize, x: int = defaultXPosition,
                 y: int = defaultYPosition, anchor: str = defaultAnchor):
        super().__init__()
        self.anchor = anchor
        self.font = font
        self.text = text
        self.size = size
        self.x = x
        self.y = y

    def __str__(self):
        return f'Text Instruction, Font: {self.font}, Text: {self.text}, Size: {self.size}, X: {self.x}, Y: {self.y},' \
               f' Anchor: {self.anchor}'


class NewPageInstruction(Instruction):
    """An instruction which tells the program to create a new, blank page"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'New Page Instruction, no parameters'


class ImageInstruction(Instruction):
    """An instruction which tells the program to add an image with parameters"""
    def __init__(self, directory: str = "", x: int = defaultXPosition, y: int = defaultYPosition,
                 width: int = defaultImageWidth, height: int = defaultImageHeight):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.directory = directory

    def __str__(self):
        return f'Image Instruction, Directory: {self.directory}, X: {self.x}, Y: {self.y}, Width: {self.width}' \
               f', Height: {self.height}'


class LineInstruction(Instruction):
    """An instruction which tells the program to draw a line across the document"""
    def __init__(self, y: int = defaultYPosition, size: int = defaultLineSize):
        super().__init__()
        self.y = y
        self.size = size

    def __str__(self):
        return f'Line Instruction, Y: {self.y}, Size: {self.size}'


class TableInstruction(Instruction):
    def __init__(self, font: str = defaultFont, x: int = defaultXPosition, y: int = defaultYPosition,
                 font_size: int = defaultTextSize, column_width: int = defaultColumnWidth,
                 column_height: int = defaultColumnHeight, texts: list[list[str]] = None):
        super().__init__()
        self.font = font
        self.texts = texts
        self.x = x
        self.y = y
        self.fontSize = font_size
        self.columnWidth = column_width
        self.columnHeight = column_height

    def __str__(self):
        return f'Table Instruction, Font: {self.font}, X: {self.x}, Y: {self.y}, Column Width: {self.columnWidth}, ' \
               f'Column Height: {self.columnHeight},Font Size: {self.fontSize}, Texts: {self.texts}'
