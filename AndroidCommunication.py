#!/usr/bin/env python

import socket
import base64, os
from pytesseract import *
from PIL import Image

host = ''
port = 50000
backlog = 5
size = 8192
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
outputfilename = "out.txt"
while 1:
    try:
        client, address = s.accept()
        data = client.recv(size)
        print()
        print()
        print ("INSTRUCTION: ", data.decode('utf-8'))
        if data.decode('utf-8') == "Send Image":  
            print("Function: Receiving Image Image")
            count = 0
            try:
                print("Removed old JPGfile")
                os.remove("test.jpg")
            except OSError:
                pass
            
            with open("test.jpg", "ba") as myfile:
                while data:
                    data = client.recv(size)
                    myfile.write(data)
                myfile.close()
            client.close()
            print("Done Reading in File")

            print("Obtaining words from image")
            out_string = image_to_string(Image.open('test.jpg'))
            outfile = open(outputfilename, 'w')
            outfile.write(out_string)
            outfile.close()
            print("Done Converting picture over")
        elif data.decode('utf-8') == "Send Text":
            print("Function: Receive Text From Android")
            try:
                os.remove(outputfilename)
            except OSError:
                pass
            with open(outputfilename, "ba") as myfile:
                while data:
                    data = client.recv(size)
                    myfile.write(data)
                myfile.close()
            client.close()
            print("Done Receiving Text")
        elif data.decode('utf-8') == "Receive Text":
            print("Function: Send Text To Android")
            with open(outputfilename, 'r') as infile:
                d = infile.read(1024)
                while d:
                    client.send(d.encode('utf-8'))
                    d = infile.read(1024)
            client.close()
            print("Done Sending Text")
    except:
        print("INSTRUCTION: FALSE")
        client.close()
    
    
    
