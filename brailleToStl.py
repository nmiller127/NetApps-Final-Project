import stl, numpy
from math import floor
from stl import mesh

#GLOBAL DIMENSIONS FOR EACH CHARACTER
CHAR_X = 6.4
CHAR_Y = 10
CHAR_Z = 0.3
MAX_X = 234
MAX_Y = 196

#TILE DIMENSIONS
TOP_TO_DOT_CENTER = 2.6 #mm
DOT_CENTER_TO_DOT_CENTER = 2.4
SIDE_TO_DOT_CENTER = 2 #mm

def getDimensions(brailleList):
    charsPerLine = floor(MAX_Y / CHAR_Y) #the number of characters that can fit on a line using the given max size and tile dimensions
    linesPerSheet = floor(MAX_X / CHAR_X)   #the number of lines that can fit on a sheet using the given max size and tile dimensions
    totalChars = charsPerLine * linesPerSheet #The maximum number of characters that can fit on a sheet
    chars = 1
    lines = 1

    messageLength = len(brailleList) #The length of the input string
    print("String Length: ",messageLength)

    if (messageLength < charsPerLine):
        chars = messageLength
        print("Single line input")
    else:
        chars = charsPerLine
        lines = floor(messageLength/charsPerLine)
        print("Lines needed: ", lines)
    return chars, lines


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
        translate(dot_copy, 2.6 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 2 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[1]): #dot2
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, 5 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 2 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[2]): #dot3
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, 7.4 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 2 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[3]): #dot4
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, 2.6 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 4.4 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[4]): #dot5
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, 5 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 4.4 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    if (letter[5]): #dot6
        dot_copy = mesh.Mesh(obj.data.copy())
        translate(dot_copy, 7.4 + (10 * lineOffset), 0, 1, 'x')
        translate(dot_copy, 4.4 + (6.4 * charOffset), 0, 1, 'y')
        translate(dot_copy, h1, 0, 1, 'z')
        dotGroup.append(dot_copy)
    return dotGroup

#####################################################
#### TESTING
#####################################################
brailleList = [(True, False, False, False, False, False),
            (True, True, False, False, False, False),
            (True, False, False, True, False, False),
            (True, False, False, True, True, False),
            (True, False, False, False, True, False),
            (True, True, False, True, False, False),
            (True, True, False, True, True, False),
            (True, True, False, False, True, False),
            (False, True, False, True, False, False),
            (False, True, False, True, True, False),
            (True, False, True, False, False, False),
            (True, True, True, False, False, False),
            (True, False, True, True, False, False),
            (True, False, True, True, True, False),
            (True, False, True, False, True, False),
            (True, True, True, True, False, False),
            (True, True, True, True, True, False),
            (True, True, True, False, True, False),
            (False, True, True, True, False, False),
            (False, True, True, True, True, False),
            (True, False, True, False, False, True),
            (True, True, True, False, False, True),
            (False, True, False, True, True, True),
            (True, False, True, True, False, True),
            (True, False, True, True, True, True),
            (True, False, True, False, True, True),
            (False, False, False, False, False, True), (True, False, False, False, False, False),
            (False, False, False, False, False, True), (True, True, False, False, False, False),
            (False, False, False, False, False, True), (True, False, False, True, False, False),
            (False, False, False, False, False, True), (True, False, False, True, True, False),
            (False, False, False, False, False, True), (True, False, False, False, True, False),
            (False, False, False, False, False, True), (True, True, False, True, False, False),
            (False, False, False, False, False, True), (True, True, False, True, True, False),
            (False, False, False, False, False, True), (True, True, False, False, True, False),
            (False, False, False, False, False, True), (False, True, False, True, False, False),
            (False, False, False, False, False, True), (False, True, False, True, True, False),
            (False, False, False, False, False, True), (True, False, True, False, False, False),
            (False, False, False, False, False, True), (True, True, True, False, False, False),
            (False, False, False, False, False, True), (True, False, True, True, False, False),
            (False, False, False, False, False, True), (True, False, True, True, True, False),
            (False, False, False, False, False, True), (True, False, True, False, True, False),
            (False, False, False, False, False, True), (True, True, True, True, False, False),
            (False, False, False, False, False, True), (True, True, True, True, True, False),
            (False, False, False, False, False, True), (True, True, True, False, True, False),
            (False, False, False, False, False, True), (False, True, True, True, False, False),
            (False, False, False, False, False, True), (False, True, True, True, True, False),
            (False, False, False, False, False, True), (True, False, True, False, False, True),
            (False, False, False, False, False, True), (True, True, True, False, False, True),
            (False, False, False, False, False, True), (False, True, False, True, True, True),
            (False, False, False, False, False, True), (True, False, True, True, False, True),
            (False, False, False, False, False, True), (True, False, True, True, True, True),
            (False, False, False, False, False, True), (True, False, True, False, True, True),
            (False, False, True, True, True, True), (True, False, False, False, False, False),
            (False, False, True, True, True, True), (True, True, False, False, False, False),
            (False, False, True, True, True, True), (True, False, False, True, False, False),
            (False, False, True, True, True, True), (True, False, False, True, True, False),
            (False, False, True, True, True, True), (True, False, False, False, True, False),
            (False, False, True, True, True, True), (True, True, False, True, False, False),
            (False, False, True, True, True, True), (True, True, False, True, True, False),
            (False, False, True, True, True, True), (True, True, False, False, True, False),
            (False, False, True, True, True, True), (False, True, False, True, False, False),
            (False, False, True, True, True, True), (False, True, False, True, True, False),
            (False, False, False, False, False, False),
            (False, True, False, False, True, True),
            (False, True, False, False, False, False),
            (False, True, True, False, False, False),
            (False, True, False, False, True, False),
            (False, False, True, False, False, False),
            (False, False, True, False, False, True),
            (False, True, True, False, True, False),
            (False, True, True, False, False, True)]#,
            #'\n']

charsNeeded, linesNeeded = getDimensions(brailleList)
print("Chars needed: ", charsNeeded, " Lines Needed: ", linesNeeded)
createBase(charsNeeded, linesNeeded)

# Using an existing stl file:
base = mesh.Mesh.from_file('tablet_template.stl')

# rotate along Y
#main_body.rotate([0.0, 0.5, 0.0], math.radians(90))

minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(base)
w1 = maxx - minx
l1 = maxy - miny
h1 = maxz - minz
#copies = copy_obj(base, (w1, l1, h1), 4, 2, 1)
#not making any copies

# I wanted to add another related STL to the final STL
dot = mesh.Mesh.from_file('braille_dot.stl')
dot2 = mesh.Mesh.from_file('braille_dot.stl')
dot3 = mesh.Mesh.from_file('braille_dot.stl')
dot4 = mesh.Mesh.from_file('braille_dot.stl')
dot5 = mesh.Mesh.from_file('braille_dot.stl')
dot6 = mesh.Mesh.from_file('braille_dot.stl')

minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(dot)
w2 = maxx - minx
l2 = maxy - miny
h2 = maxz - minz

letter1 = makeLetter(dot, (w2, l2, h2), (True, False, True, False, True, True), 0, 0)
letter2 = makeLetter(dot, (w2, l2, h2), (True, True, False, False, False, True), 1, 0)
letter3 = makeLetter(dot, (w2, l2, h2), (True, False, True, False, True, True), 1, 1)

letterList = list()
for line in range(0, linesNeeded):
    for letter in range(0, charsNeeded):
        letterList.append(makeLetter(dot, (w2, l2, h2), brailleList[letter + (charsNeeded * line)], letter, line))
        print("Line: ", line, " Letter: ", letter)


#array1 = (letter1, letter2, letter3)
#combined = mesh.Mesh(numpy.concatenate([base.data] + [dot.data for dot in lettertest] + [dot.data for dot in lettertest3] + [dot.data for dot in lettertest2])) # +
combined = mesh.Mesh(numpy.concatenate([base.data] + [dot.data for letter in letterList for dot in letter])) # +
                                   # [copy.data for copy in copies2]))

combined.save('combined.stl', mode=stl.Mode.ASCII)  # save as#  ASCII


#FIX: Base size isn't correct. fix dimensions or labelling
#FIX: combining elements of the array at the end
