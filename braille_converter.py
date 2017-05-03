#!/usr/bin/python

class Braille_Converter(object):
    def __init__(self):
        """ Constructor for the Braille_Converter. """

        # Dictionary for single lower-case Braille characters.
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

        # Dictionary for single upper-case Braille characters. Assumes that the
        #     captial modifier is used before directly converting to this
        #     dictionary.
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

        # Dicitonary for single number Braille characters. Assumes that the
        #     number modifier is used before directly converting to this
        #     dictionary.
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

        # Dictionary for punctuation Braille characters. Punctuation that is
        #      context sensitive has another level of dictionary to distiguish.
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
                        '\n': '\n',
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

        # Dictionary for Braille modifiers.
        self.mod_dict = {'_name': 'Modifier Dictionary',
                         'upper-case': (False, False, False, False, False, True),
                         'multi-upper-case': [(False, False, False, False, False, True), (False, False, False, False, False, True)],
                         'number': (False, False, True, True, True, True)}

        # Member that holds the converted Braille characters so that any
        #      method can access this list.
        self.out = list()

    def is_punc(self, in_word):
        """ Return boolean indicating whether in_word is all punctuation.

        Keyword arguments:
        in_word -- string that method tests
        """
        for char in in_word:
            try:
                defined = self.punc_dict[char]
            except KeyError:
                return False
            else:
                continue
        return True

    def is_upper(self, in_word):
        """ Return boolean indicating whether in_word is all upper-case.

        Method ignores punctuation.

        Keyword arguments:
        in_word -- string that method tests
        """
        for char in in_word:
            try:
                defined = self.upper_case_dict[char]
            except KeyError:
                if self.is_punc(char):
                    continue
                else:
                    return False
        return True

    def is_number(self, in_word):
        """ Return boolean indicating whether in_word is all numbers.

        Method ignores punctuation.

        Keyword arguments:
        in_word -- string that method tests
        """
        for char in in_word:
            try:
                defined = self.number_dict[char]
            except KeyError:
                if self.is_punc(char):
                    continue
                else:
                    return False
        return True

    def append_def(self, char, dctnry, word="", index=None):
        """ Append the definition for char in dctnry to self.out

        Keyword arguments:
        char -- key to look for in dctnry
        dctnry -- dictionary to look in
        word -- word that the char appears inside of (for context)
        index -- where in the word that the char appears inside of
        """
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
                    print("[ ] Found a badly placed ' \" ' in: " + word)
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
            print("[x] Added cell [" + char + "] from " + dctnry['_name'])

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
