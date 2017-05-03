import textToSTL as translator
import PrinterControl as octopi

print('Enter text to translate:')
text = input()
filename = translator.textToSTL(text)
octopi.print_stl_file(filename)