#####################################
# DOCUMENT ACER CREATED BY ELLIOACE #
#####################################
import time

from PIL import Image, ImageDraw, ImageFont
import os
from acedocument import parser, document_default
from acedocument.instruction import *

version = '0.2'
print('########################################################')
print(f'# DOCUMENT ACER VERSION {version} CREATED BY ELLIOACE #')
print('########################################################')

documentDirectory = 'document'
inputDirectory = fr'{documentDirectory}\index.acedoc'
tempDirectory = fr'{documentDirectory}\indexTemp.acetemp'
outputDirectory = r'out\page'
imageDirectory = fr'{documentDirectory}\images'

errorCount = 0

time.sleep(3)

print("If you are new to document acer and it's syntax, review the documentation provided")
print("Beginning compilation in 3 seconds")

time.sleep(3)

pageSize = (2480, 3580)

# Get all the fonts from the operating system
fontList = os.listdir(r'C:\Windows\fonts')

# Set the current directory of os to be here
os.curdir = dir()

# Get the input file
try:
    indexIn = open(inputDirectory, encoding='utf-8')
except FileNotFoundError:
    print(f"CRITICAL ERROR: FILE NOT FOUND! FILE DIRECTORY: {inputDirectory}")
    exit(1)

# Remove the temporary index file in-case the program crashed, and it still remains
if os.path.exists(tempDirectory):
    os.remove(tempDirectory)
    print(f"Found {tempDirectory}! Removing...")

# Create a temporary index to read from, which ignores all comments
try:
    indexRead = open(tempDirectory, 'x')
except FileExistsError:
    print(f"CRITICAL ERROR: FILE ALREADY EXISTS! FILE DIRECTORY: {tempDirectory}")
    exit(1)

# Write to the temporary file
for line in indexIn.readlines():
    if line[0] != '#':
        indexRead.write(line)


def get_temporary_index():
    """Get the temporary index that the program should read from"""
    global indexRead
    indexRead.close()
    indexRead = open(tempDirectory)
    return indexRead


document_default.__init__(get_temporary_index())

defaultSize: int = document_default.defaultTextSize

pages: list[Image] = []


def new_page_image():
    """Returns a new blank page"""
    return Image.new("RGB", pageSize, "white")


currentPage: Image = new_page_image()

pages.append(currentPage)

# Creates a new page and carries on further instructions
def add_new_page():
    """Add a new page to the list of pages and set it as the current page"""
    global currentPage
    currentPage = new_page_image()
    if pages.__contains__(currentPage) is False:
        pages.append(currentPage)


# Adds text to the page at a specified x and y with a specified size
def add_text(font: str, text: str = "", x: int = document_default.defaultXPosition,
             y: int = document_default.defaultYPosition, size: int = defaultSize, page: Image = currentPage,
             anchor: str = document_default.defaultAnchor):
    global errorCount
    """Add text to the current page"""
    draw = ImageDraw.Draw(page)
    if fontList.__contains__(font):
        print("Provided font is valid!")
    else:
        errorCount += 1
        print(f"ERROR: FONT INVALID! PROVIDED FONT: {font}")
        return
    try:
        if anchor != "LEFT" and anchor != "CENTER" and anchor != "RIGHT":
            raise ValueError(f"INVALID ANCHOR ARGUMENT: {anchor}")
        sizedfont = ImageFont.truetype(font, size)
        if anchor == "RIGHT":
            x += pageSize[0] - sizedfont.getlength(text)
        elif anchor == "CENTER":
            x += (pageSize[0] - sizedfont.getlength(text)) / 2
        draw.text((x, y), text, font=sizedfont, fill="black")
    except ValueError as e:
        errorCount += 1
        print("Invalid text instruction argument. Info: " + e.__str__())
        return


def add_image(directory: str, x: int = document_default.defaultXPosition,
              y: int = document_default.defaultYPosition, width: int = document_default.defaultImageWidth,
              height: int = document_default.defaultImageHeight, page: Image = currentPage):
    image = Image.open(fr'{imageDirectory}\{directory}')
    image = image.resize((width, height))
    page.paste(image, (x, y))


def draw_line(y: int = document_default.defaultYPosition, size: int = document_default.defaultLineSize,
              page: Image = currentPage):
    draw = ImageDraw.Draw(page)
    draw.line(((0, y), (pageSize[0], y)), "black", size)


def draw_table(font: str, x: int = document_default.defaultXPosition, y: int = document_default.defaultYPosition,
               font_size: int = document_default.defaultTextSize,
               column_width: int = document_default.defaultColumnWidth,
               column_height: int = document_default.defaultColumnHeight,
               texts: list[list[str]] = None, page: Image = currentPage):
    global errorCount
    try:
        if texts is None:
            raise ValueError("There is no text within this table. Continuing to next instruction.")
    except ValueError as e:
        print(e)
        errorCount += 1
        return
    draw = ImageDraw.Draw(page)
    y_addition = 0
    x_addition = -column_width
    sized_font = ImageFont.truetype(font, font_size)
    for sections in texts:
        biggest_addition = 0
        for text in sections:
            current_line = ""
            text_with_lines = ""
            for char in text:
                if sized_font.getlength(current_line) > column_width - font_size:
                    text_with_lines += '\n'
                    current_line = ""
                text_with_lines += char
                current_line += char
            added_size = font_size * 0.75 * text_with_lines.count('\n')
            if added_size > biggest_addition:
                biggest_addition = added_size
        section_column_height = column_height + biggest_addition
        for text in sections:
            x_addition += column_width
            added_x = x + x_addition
            added_y = y + y_addition
            longest_line = ""
            current_line = ""
            text_with_lines = ""
            for char in text:
                if sized_font.getlength(current_line) > column_width - font_size:
                    if sized_font.getlength(current_line) > sized_font.getlength(longest_line):
                        longest_line = current_line
                    text_with_lines += '\n'
                    current_line = ""
                text_with_lines += char
                current_line += char
            if longest_line == "":
                longest_line = text
            center_position = round((column_width - sized_font.getlength(longest_line)) / 2)
            add_text(font, text_with_lines, added_x + center_position, added_y + round(column_height / 4), font_size,
                     page, "LEFT")
            draw.rectangle((added_x, added_y, added_x + column_width, added_y + section_column_height),
                           outline="black", width=15)
        y_addition += section_column_height
        x_addition = -column_width


# Do the final tasks before closing the script
def finish():
    """Finish the program by doing any final tasks"""
    pagenumber = 1
    for page in pages:
        page.save(fr'{outputDirectory}{pagenumber}.png')
        pagenumber += 1
    indexRead.close()
    os.remove(tempDirectory)
    print("\nCompilation complete!")
    if errorCount == 0:
        print("No issues found. If the document is not the expected result, check your index file for mistakes")
    else:
        print(f"{errorCount} {'error was' if errorCount == 1 else 'errors were'} encountered during compilation. "
              f"Please check the debug logs and fix any issues.")


for line in get_temporary_index():
    try:
        instruction = parser.parseline(line)
    except ValueError:
        errorCount += 1
        print(f"Error at line: {line}. Reason: Value error, make sure your values are correct here.".replace('\n', ''))
        continue

    print(instruction)
    if isinstance(instruction, TextInstruction):
        add_text(instruction.font, instruction.text, instruction.x, instruction.y, instruction.size, currentPage,
                 instruction.anchor)
    elif isinstance(instruction, NewPageInstruction):
        add_new_page()
    elif isinstance(instruction, ImageInstruction):
        add_image(instruction.directory, instruction.x, instruction.y, instruction.width, instruction.height,
                  currentPage)
    elif isinstance(instruction, LineInstruction):
        draw_line(instruction.y, instruction.size, currentPage)
    elif isinstance(instruction, TableInstruction):
        draw_table(instruction.font, instruction.x, instruction.y, instruction.fontSize, instruction.columnWidth,
                   instruction.columnHeight, instruction.texts, currentPage)

finish()
