import stl, numpy
#from numpy import stl
from math import floor, ceil
from stl import mesh

class Braille_Converter(object):
    def __init__(self):
        # Dictionary for single Braille characters
        self.lower_case_dict = {'_name': 'Lower-case Dictionary',
                        'a': (True, False, False, False, False, False),
                        'b': (True, True, False, False, False, False),
                        'c': (True, False, False, True, False, False),
                        'd': (True, False, False, True, True, False),
                        'e': (True, False, False, False, True, False),
                        'f': (True, True, False, True, False, False),
                        'g': (True, True, False, True, True, False),
                        'h': (True, True, False, False, True, False),
                        'i': (False, True, False, True, False, False),
                        'j': (False, True, False, True, True, False),
                        'k': (True, False, True, False, False, False),
                        'l': (True, True, True, False, False, False),
                        'm': (True, False, True, True, False, False),
                        'n': (True, False, True, True, True, False),
                        'o': (True, False, True, False, True, False),
                        'p': (True, True, True, True, False, False),
                        'q': (True, True, True, True, True, False),
                        'r': (True, True, True, False, True, False),
                        's': (False, True, True, True, False, False),
                        't': (False, True, True, True, True, False),
                        'u': (True, False, True, False, False, True),
                        'v': (True, True, True, False, False, True),
                        'w': (False, True, False, True, True, True),
                        'x': (True, False, True, True, False, True),
                        'y': (True, False, True, True, True, True),
                        'z': (True, False, True, False, True, True)}

        self.upper_case_dict = {'_name': 'Upper-case Dictionary',
                        'A': (True, False, False, False, False, False),
                        'B': (True, True, False, False, False, False),
                        'C': (True, False, False, True, False, False),
                        'D': (True, False, False, True, True, False),
                        'E': (True, False, False, False, True, False),
                        'F': (True, True, False, True, False, False),
                        'G': (True, True, False, True, True, False),
                        'H': (True, True, False, False, True, False),
                        'I': (False, True, False, True, False, False),
                        'J': (False, True, False, True, True, False),
                        'K': (True, False, True, False, False, False),
                        'L': (True, True, True, False, False, False),
                        'M': (True, False, True, True, False, False),
                        'N': (True, False, True, True, True, False),
                        'O': (True, False, True, False, True, False),
                        'P': (True, True, True, True, False, False),
                        'Q': (True, True, True, True, True, False),
                        'R': (True, True, True, False, True, False),
                        'S': (False, True, True, True, False, False),
                        'T': (False, True, True, True, True, False),
                        'U': (True, False, True, False, False, True),
                        'V': (True, True, True, False, False, True),
                        'W': (False, True, False, True, True, True),
                        'X': (True, False, True, True, False, True),
                        'Y': (True, False, True, True, True, True),
                        'Z': (True, False, True, False, True, True)}

        self.number_dict = {'_name': 'Number Dictionary',
                        '1': (True, False, False, False, False, False),
                        '2': (True, True, False, False, False, False),
                        '3': (True, False, False, True, False, False),
                        '4': (True, False, False, True, True, False),
                        '5': (True, False, False, False, True, False),
                        '6': (True, True, False, True, False, False),
                        '7': (True, True, False, True, True, False),
                        '8': (True, True, False, False, True, False),
                        '9': (False, True, False, True, False, False),
                        '0': (False, True, False, True, True, False)}

        self.punc_dict = {'_name': 'Punctuation Dictionary',
                        ' ': (False, False, False, False, False, False),
                        '*': [(False, False, True, False, True, False), (False, False, True, False, True, False)],
                        '[': [(False, False, False, False, False, True), (False, True, True, False, True, True)],
                        ']': [(False, True, True, False, True, True), (False, False, False, False, False, True)],
                        ':': (False, True, False, False, True, False),
                        ',': (False, True, False, False, False, False),
                        '$': [(False, True, False, False, True, True), (False, False, True, True, True, True)],
                        '...': [(False, False, True, False, False, False), (False, False, True, False, False, False), (False, False, True, False, False, False)],
                        '!': (False, True, True, False, True, False),
                        '(': (False, True, True, False, True, True),
                        ')': (False, True, True, False, True, True),
                        '?': (False, True, True, False, False, True),
                        ';': (False, True, True, False, False, False),
                        '\n': [(False, False, False, False, False, False), (False, False, False, False, False, False)],
                        "'": {'_name': '[ \' ] Dictionary',
                              'apostrophe': (False, False, True, False, False, False),
                              'single-quote-left': [(False, False, False, False, False, True), (False, True, True, False, False, True)],
                              'single-quote-right': [(False, False, True, False, True, True), (False, False, True, False, False, False)]},
                        '"': {'_name': '[ " ] Dictionary',
                              'double-quote-left': (False, True, True, False, False, True),
                              'double-quote-right': (False, False, True, False, True, True)},
                        '-': {'_name': '[ - ] Dictionary',
                              'hyphen': (False, False, True, False, False, True),
                              'dash': [(False, False, True, False, False, True), (False, False, True, False, False, True)]},
                        '.': {'_name': '[ . ] Dictionary',
                              'period': (False, True, False, False, True, True),
                              'decimal': (False, False, False, True, False, True)}}

        self.mod_dict = {'_name': 'Modifier Dictionary',
                         'upper-case': (False, False, False, False, False, True),
                         'multi-upper-case': [(False, False, False, False, False, True), (False, False, False, False, False, True)],
                         'number': (False, False, True, True, True, True)}

        self.out = list()

    def is_upper(self, in_word):
        for char in in_word:
            try:
                defined = self.upper_case_dict[char]
            except KeyError:
                try:
                    defined = self.punc_dict[char]
                except KeyError:
                    return False
                else:
                    continue
        return True

    def is_number(self, in_word):
        for char in in_word:
            try:
                defined = self.number_dict[char]
            except KeyError:
                try:
                    defined = self.punc_dict[char]
                except KeyError:
                    return False
                else:
                    continue
        return True

    def is_punc(self, in_word):
        for char in in_word:
            try:
                defined = self.punc_dict[char]
            except KeyError:
                try:
                    defined = self.punc_dict[char]
                except KeyError:
                    return False
                else:
                    continue
        return True

    def append_def(self, char, dctnry, word="", index=None):
        if type(dctnry[char]) is list:
            for cell in dctnry[char]:
                self.out.append(cell)
            print("[x] Added cell [" + char + "] from " + dctnry['_name'])

        elif type(dctnry[char]) is dict:

            if char == "'":
                if index == 0:
                    self.append_def('single-quote-left', self.punc_dict["'"])
                elif index == (len(word) - 1):
                    self.append_def('single-quote-right', self.punc_dict["'"])
                else:
                    self.append_def('apostrophe', self.punc_dict["'"])

            elif char == '"':
                if index == 0:
                    self.append_def('double-quote-left', self.punc_dict['"'])
                elif index == (len(word) - 1) or self.is_punc(word[index+1:]):
                    self.append_def('double-quote-right', self.punc_dict['"'])
                else:
                    print("[ ] Found a badly placed '\"' in: " + word)
                    self.out.append('BAD DOUBLE QUOTE')

            elif char == '-':
                if index == 0:
                    self.append_def('dash', self.punc_dict['-'])
                else:
                    self.append_def('hyphen', self.punc_dict['-'])

            elif char == '.':
                if index == (len(word) - 1):
                    self.append_def('period', self.punc_dict['.'])
                else:
                    self.append_def('decimal', self.punc_dict['.'])

        else:
            self.out.append(dctnry[char])
            #print("[x] Added cell [" + char + "] from " + dctnry['_name'])

    def grade_1_convert(self, in_text):
        words = in_text.split(' ')
        for word in words:
            index = 0
            # Check if word is all upper case
            if(self.is_upper(word)):
                self.append_def('multi-upper-case', self.mod_dict)
                for char in word:
                    try:
                        self.append_def(char, self.upper_case_dict)
                    except KeyError:
                        self.append_def(char, self.punc_dict, word, index)
                    index = index + 1

            # Check if word is all numbers
            elif(self.is_number(word)):
                self.append_def('number', self.mod_dict)
                for num in word:
                    try:
                        self.append_def(num, self.number_dict)
                    except KeyError:
                        self.append_def(num, self.punc_dict, word, index)
                    index = index + 1

            else:
                for char in word:
                    try:
                        self.append_def(char, self.lower_case_dict)
                    except KeyError:
                        try:
                            cell = self.upper_case_dict[char]
                        except KeyError:
                            self.append_def(char, self.punc_dict, word, index)
                        else:
                            self.append_def('upper-case', self.mod_dict)
                            self.append_def(char, self.upper_case_dict)
                    index = index + 1

            self.append_def(' ', self.punc_dict)


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
    lines = 1
    #print("Chars per line = ", charsPerLine, " Lines Per Sheet = ", linesPerSheet)
    messageLength = len(brailleList) #The length of the input string
    #print("String Length: ", messageLength)

    if (messageLength < charsPerLine):
        chars = messageLength
    else:
        chars = charsPerLine
        lines = ceil(messageLength/charsPerLine)
    return chars, lines

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
    charsNeeded, linesNeeded = getDimensions(brailleList) #get the size of the base

    brailleList, linesNeeded = fixSpacing(brailleList, 30, 23)

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
    converter = Braille_Converter()

    # converter.grade_1_convert('"This is NUTS, man...", said George as 150.123 rocks rolled down the hill.')
    converter.grade_1_convert(text)
    return brailleToSTL(converter.out)

#####################################################
#### TESTING
#####################################################

#stlFile = textToSTL("Controllers received signals from Cassini early Thursday after it made its first pass between Saturn's cloud tops and the inner edge of the planet's rings. The spacecraft was out of radio contact with Earth during the close approach. Cassini is now in the \"Grand Finale\" phase of its mission, with 22 close approaches planned before the mission ends with a dive into the planet's atmosphere in September. See more at: spacenews.com")
#print("File created: ",stlFile)
