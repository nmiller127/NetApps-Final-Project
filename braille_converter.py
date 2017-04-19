#!/usr/bin/python

import sys

class Braille_Converter(object):
    def __init__(self):
        # Dictionary for single Braille characters
        self.low_case_alpha = {'a': (True, False, False, False, False, False),
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

        self.up_case_alpha = {'A': [(False, False, False, False, False, True), (True, False, False, False, False, False)],
                        'B': [(False, False, False, False, False, True), (True, True, False, False, False, False)],
                        'C': [(False, False, False, False, False, True), (True, False, False, True, False, False)],
                        'D': [(False, False, False, False, False, True), (True, False, False, True, True, False)],
                        'E': [(False, False, False, False, False, True), (True, False, False, False, True, False)],
                        'F': [(False, False, False, False, False, True), (True, True, False, True, False, False)],
                        'G': [(False, False, False, False, False, True), (True, True, False, True, True, False)],
                        'H': [(False, False, False, False, False, True), (True, True, False, False, True, False)],
                        'I': [(False, False, False, False, False, True), (False, True, False, True, False, False)],
                        'J': [(False, False, False, False, False, True), (False, True, False, True, True, False)],
                        'K': [(False, False, False, False, False, True), (True, False, True, False, False, False)],
                        'L': [(False, False, False, False, False, True), (True, True, True, False, False, False)],
                        'M': [(False, False, False, False, False, True), (True, False, True, True, False, False)],
                        'N': [(False, False, False, False, False, True), (True, False, True, True, True, False)],
                        'O': [(False, False, False, False, False, True), (True, False, True, False, True, False)],
                        'P': [(False, False, False, False, False, True), (True, True, True, True, False, False)],
                        'Q': [(False, False, False, False, False, True), (True, True, True, True, True, False)],
                        'R': [(False, False, False, False, False, True), (True, True, True, False, True, False)],
                        'S': [(False, False, False, False, False, True), (False, True, True, True, False, False)],
                        'T': [(False, False, False, False, False, True), (False, True, True, True, True, False)],
                        'U': [(False, False, False, False, False, True), (True, False, True, False, False, True)],
                        'V': [(False, False, False, False, False, True), (True, True, True, False, False, True)],
                        'W': [(False, False, False, False, False, True), (False, True, False, True, True, True)],
                        'X': [(False, False, False, False, False, True), (True, False, True, True, False, True)],
                        'Y': [(False, False, False, False, False, True), (True, False, True, True, True, True)],
                        'Z': [(False, False, False, False, False, True), (True, False, True, False, True, True)]}

        self.number_dict = {'1': [(False, False, True, True, True, True), (True, False, False, False, False, False)],
                        '2': [(False, False, True, True, True, True), (True, True, False, False, False, False)],
                        '3': [(False, False, True, True, True, True), (True, False, False, True, False, False)],
                        '4': [(False, False, True, True, True, True), (True, False, False, True, True, False)],
                        '5': [(False, False, True, True, True, True), (True, False, False, False, True, False)],
                        '6': [(False, False, True, True, True, True), (True, True, False, True, False, False)],
                        '7': [(False, False, True, True, True, True), (True, True, False, True, True, False)],
                        '8': [(False, False, True, True, True, True), (True, True, False, False, True, False)],
                        '9': [(False, False, True, True, True, True), (False, True, False, True, False, False)],
                        '0': [(False, False, True, True, True, True), (False, True, False, True, True, False)]}

        self.puct_dict = {' ': (False, False, False, False, False, False),
                        "'": (False, False, True, False, False, False),
                        '*': [(False, False, True, False, True, False), (False, False, True, False, True, False)],
                        '[': [(False, False, False, False, False, True), (False, True, True, False, True, True)],
                        ']': [(False, True, True, False, True, True), (False, False, False, False, False, True)],
                        ':': (False, True, False, False, True, False),
                        ',': (False, True, False, False, False, False),
                        '-': (False, False, True, False, False, True), #TODO: hyphen and dash are different!?
                        '$': [(False, True, False, False, True, True), (False, False, True, True, True, True)],
                        '...': [(False, False, True, False, False, False), (False, False, True, False, False, False), (False, False, True, False, False, False)],
                        '!': (False, True, True, False, True, False),
                        '.': (False, True, False, False, True, True),
                        ';': (False, True, True, False, False, False),
                        '\'': (False, False, True, False, False, False),
                        '?': (False, True, True, False, False, True),
                        '\n': '\n'}


    def grade_1_convert(self, in_text):
        out = list()
        for char in in_text:
            if(type(self.grade_1_dict[char]) is list):
                for cell in self.grade_1_dict[char]:
                    out.append(cell)
            else:
                out.append(self.grade_1_dict[char])

        return out

""" TESTING SCRIPT """

converter = Braille_Converter()
in_text = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 .,;:'-!?\n"
out = converter.grade_1_convert(in_text)

correct_out = [(True, False, False, False, False, False),
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
            (False, True, True, False, False, True),
            '\n']

i = 0
for cell in correct_out:
    if(correct_out[i] == out[i]):
        continue
    else:
        print("Error in cell '" + str(i) + "':\n Out:     " + str(out[i]) + "\n Correct: " + str(cell))
    i = i + 1
