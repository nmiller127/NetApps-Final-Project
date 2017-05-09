#!/usr/bin/python3

import stl, numpy
from math import floor, ceil
from stl import mesh
from braille_converter import Braille_Converter

#GLOBAL DIMENSIONS FOR EACH CHARACTER
CHAR_X = 6.4    #Character WIDTH (orig = 6.4mm)
CHAR_Y = 10     #Character HEIGHT (orig = 10mm)
CHAR_Z = 0.3    #Character vertical height (orig = 0.3mm)
MAX_Y = 234     #max = 234 PAPER HEIGHT
MAX_X = 196     #max = 196 PAPER WIDTH

#TILE DIMENSIONS
TOP_TO_DOT_CENTER = 2.6         #2.6mm default
DOT_CENTER_TO_DOT_CENTER = 2.4  #2.4mm default
SIDE_TO_DOT_CENTER = 2          #2mm default


def getDimensions(brailleList):
    charsPerLine = floor(MAX_X / CHAR_X) #the number of characters that can fit on a line using the given max size and tile dimensions
    linesPerSheet = floor(MAX_Y / CHAR_Y)   #the number of lines that can fit on a sheet using the given max size and tile dimensions
    totalChars = charsPerLine * linesPerSheet #The maximum number of characters that can fit on a sheet
    chars = 1
    #print("Chars per line = ", charsPerLine, " Lines Per Sheet = ", linesPerSheet)
    messageLength = len(brailleList) #The length of the input string
    #print("String Length: ", messageLength)

    if (messageLength < charsPerLine):
        chars = messageLength
    else:
        chars = charsPerLine
    return chars, linesPerSheet

# Use the dimensions to
def fixSpacing(brailleList, charsPerLine, linesPerSheet):
    space = (False, False, False, False, False, False)
    newBrailleList = list()
    wordArray = list()
    print("Fixing spacing...")

    x = 0
    #Break the list up by spaces and newlines. wordArray is the array of words in the sentence
    while (x < len(brailleList)):
        word = list()
        nextLetter = brailleList[x]
        while (nextLetter != space):
            word.append(nextLetter)
            x = x + 1
            nextLetter = brailleList[x]
        word.append(space)
        wordArray.append(word)
        #print("Word #", len(wordArray), ": ", len(word))
        x = x + 1

        if (x == len(brailleList)):
            break

    #Place words into the new array, watching out for line length
    currentPosition = 0
    currentLine = 0
    for word in range(0, len(wordArray)):
        charsLeft = charsPerLine - currentPosition
        #If the length of the word is less than the space left, add it to the array.
        #if not, move on to the next line after padding the previous one with spaces.
        if (len(wordArray[word]) <= charsLeft):
            for x in range(0, len(wordArray[word])):
                newBrailleList.append(wordArray[word][x])

            currentPosition = currentPosition + len(wordArray[word])
        else:
            #Append spaces to fill out the line
            for x in range(0, charsLeft):
                newBrailleList.append((False, False, False, False, False, False))
            currentLine = currentLine + 1
            if (currentLine > linesPerSheet):
                print("There is more text than can be printed on one sheet. The remaining text will be truncated.")
                break
            currentPosition = 0
            #Assuming the word isn't longer than an entire line
            for x in range(0, len(wordArray[word])):
                newBrailleList.append(wordArray[word][x])
            currentPosition = currentPosition + len(wordArray[word])
    return newBrailleList, currentLine

def createBase(charNum, lineNum):
    BASE_X_WIDTH = lineNum * CHAR_Y  # MAX = 234mm
    BASE_Y_WIDTH = charNum  * CHAR_X # MAX = 196mm
    BASE_Z_HEIGHT = CHAR_Z  # Height = 0.3mm

    # Define the 8 vertices of the base
    vertices = numpy.array([ \
        [0, 0, 0], [BASE_X_WIDTH, 0, 0], [BASE_X_WIDTH, BASE_Y_WIDTH, 0], [0, BASE_Y_WIDTH, 0], [0, 0, BASE_Z_HEIGHT],
        [BASE_X_WIDTH, 0, BASE_Z_HEIGHT], [BASE_X_WIDTH, BASE_Y_WIDTH, BASE_Z_HEIGHT], [0, BASE_Y_WIDTH, BASE_Z_HEIGHT]])

    # Define the 12 triangles composing the cube
    faces = numpy.array([ \
        [0, 3, 1], [1, 3, 2], [0, 4, 7], [0, 7, 3], [4, 5, 6], [4, 6, 7],
        [5, 1, 2], [5, 2, 6], [2, 3, 6], [3, 7, 6], [0, 1, 5], [0, 5, 4]])

    # Create the mesh
    rect = mesh.Mesh(numpy.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            rect.vectors[i][j] = vertices[f[j], :]

    # Write the mesh a file
    rect.save('tablet_template.stl')

# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

def translate(_solid, step, padding, multiplier, axis):
    if axis == 'x':
        items = [0, 3, 6]
    elif axis == 'y':
        items = [1, 4, 7]
    elif axis == 'z':
        items = [2, 5, 8]
    for p in _solid.points:
        # point items are ((x, y, z), (x, y, z), (x, y, z))
        for i in range(3):
            p[items[i]] += (step * multiplier) + (padding * multiplier)

def makeLetter(obj, dims, letter, charOffset, lineOffset):
    w, l, h = dims
    dotGroup = []
    if (letter[0]): #dot1
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, TOP_TO_DOT_CENTER + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[1]): #dot2
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, DOT_CENTER_TO_DOT_CENTER + TOP_TO_DOT_CENTER + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[2]): #dot3
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, DOT_CENTER_TO_DOT_CENTER + TOP_TO_DOT_CENTER*2 + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[3]): #dot4
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, TOP_TO_DOT_CENTER + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + DOT_CENTER_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[4]): #dot5
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, DOT_CENTER_TO_DOT_CENTER + TOP_TO_DOT_CENTER + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + DOT_CENTER_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[5]): #dot6
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, DOT_CENTER_TO_DOT_CENTER + TOP_TO_DOT_CENTER*2 + (CHAR_Y * lineOffset), 0, 1, 'x')
        translate(dot_copy, SIDE_TO_DOT_CENTER + DOT_CENTER_TO_DOT_CENTER + (CHAR_X * charOffset), 0, 1, 'y')
        translate(dot_copy, h, 0, 1, 'z')
        dotGroup.append(dot_copy)
    return dotGroup

def brailleToSTL(brailleList):
    stlFileName = 'braille_translation.stl'
    charsNeeded, linesPerSheet = getDimensions(brailleList) #get the size of the base

    brailleList, linesNeeded = fixSpacing(brailleList, charsNeeded, linesPerSheet)

    #Add funtion to take care of spacing of words
    length = len(brailleList)
    for x in range(0, floor(MAX_X / CHAR_X) - (length % charsNeeded)):
        brailleList.append((False, False, False, False, False, False))
    #print(floor(MAX_X / CHAR_X) - (len(brailleList) % charsNeeded))
    #print("Chars needed: ", charsNeeded, " Lines Needed: ", linesNeeded)
    createBase(charsNeeded, linesNeeded)

    base = mesh.Mesh.from_file('tablet_template.stl')

    # Open dot
    dot = mesh.Mesh.from_file('braille_dot.stl')
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(dot)
    w2 = maxx - minx
    l2 = maxy - miny
    h2 = maxz - minz

    print("Creating letters...")
    letterList = list()
    for line in range(0, linesNeeded):
        for letter in range(0, charsNeeded):
            letterList.append(makeLetter(dot, (w2, l2, h2), brailleList[letter + (charsNeeded * line)], letter, line))
            #print("Line: ", line, " Letter: ", letter)
    print("Combining meshes...")
    combined = mesh.Mesh(numpy.concatenate([base.data] + [dot.data for letter in letterList for dot in letter]))

    combined.save(stlFileName, mode=stl.Mode.ASCII)  # save as#  ASCII
    return stlFileName

def textToSTL(text):
    print("Translating text...")
    print("Text Received: " + text)
    converter = Braille_Converter()

    # converter.grade_1_convert('"This is NUTS, man...", said George as 150.123 rocks rolled down the hill.')
    converter.grade_1_convert(text)
    return brailleToSTL(converter.out)

#####################################################
#### TESTING
#####################################################

#stlFile = textToSTL("H")
#print("File created: ",stlFile)
