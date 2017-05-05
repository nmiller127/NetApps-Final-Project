import textToSTL as translator
import PrinterControl as octopi

import socket
import base64, os
from pytesseract import *
from PIL import Image

from threading import Thread
from threading import Lock

class Central_Server:
    def __init__(self):
        """ Define the server """

        # Declare socket parameters
        self.socket_host = ''
        self.socket_port = 50000
        self.socket_backlog = 5
        self.socket_size = 8192
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Initialize socket
        self.__socket.bind((self.host, self.port))

        # Declare member variables and locks to keep them thread safe
        self.image_filename = "image.jpg"
        self.image_file_lock = Lock()

        self.processed_text = ""
        self.processed_text_lock = Lock()

        print("[x] Finished initializing server.")

    def process_image(self, client):
        """ Receive and save image file from client.

        Keyword arguments:
        client -- client object returned by socket.accept()
        """
        print("[x] Receiving new image.")

        # Aquire lock on file before performing any actions on it
        print("    Acquiring lock on image file...")
        self.image_file_lock.acquire(blocking=True)
        print("[x] Acquired lock on image file.")

        # Read image in from message into new file
        print("[x] Overwriting '" + self.image_filename + "' with received image.")
        data = client.recv(size) # priming read since 'data' didn't carry over from main loop
        with open(self.image_filename, "bw") as myfile:
            while data:
                myfile.write(data)
                data = client.recv(self.socket_size)
            myfile.close()
        client.close()
        print("[x] Finished receiving and saving image.")

        # Aquire lock on processed text before performing any actions on it
        print("    Acquiring lock on processed text...")
        self.processed_text_lock.acquire(blocking=True)
        print("[x] Acquired lock on processed test.")

        # Process image and extract text, save that text to 'outputfilename'
        print("[x] Obtaining words from image.")
        self.processed_text = image_to_string(Image.open(self.image_filename))
        print("[x] Done Converting picture to text.")

        # Release locks since this thread is done with these items
        self.processed_text_lock.release()
        self.image_file_lock.release()
        print("[x] Released locks on text and image file.")

    def replace_proc_text(self, client):
        """ Receive and save confirmed text from client.

        Keyword arguments:
        client -- client object returned by socket.accept()
        """
        # If Android app is sending us confirmed text
        print("[x] Receiving text from Android.")

        # Acquire lock on processed text before performing any actions on it
        print("    Acquiring lock on processed text...")
        self.processed_text_lock.acquire(blocking=True)
        print("[x] Acquired lock on processed text.")

        # Replace processed text with text received from Android
        self.processed_text = ""
        data = client.recv(size) # priming read since 'data' didn't carry over from main loop
        while data:
            self.processed_text.append(str(data))
            data = client.recv(size)
        client.close()

        print("[x] Done receiving confirmed text.")
        print("    Starting text > Braille > STL conversion...")
        filename = translator.textToSTL(self.processed_text)
        print("[x] Completed conversion.")

        # This thread is done with text, so release lock
        self.processed_text_lock.release()

        print("    Starting 3D print...")
        octopi.print_stl_file(filename)
        print("[x] Sent instruction to OctoPi to begin 3D print.")

    def send_proc_text(self, client):
        """ If processed text is ready, send it to the client.

        Keyword arguments:
        client -- client object returned by socket.accept()
        """
        print("[x] Android requested text.")
        print("    Acquiring lock on processed text...")
        acquired = self.processed_text_lock.acquire(blocking=False)
        if acquired:
            print("[x] Acquired lock on processed text.")

            print("[x] Sending text to Android for confirmation.")
            # Send client the current processed text.
            buffer_size = 1024
            text_buffer = ""
            loop_count = len(self.processed_text) // buffer_size
            last_index = 0
            # Send the text in chunks of 'buffer_size' characters
            for i in range(loop_count):
                text_buffer = self.processed_text[(buffer_size * i):(buffer_size * (i + 1))]
                client.send(text_buffer.encode('utf-8'))
                last_index = buffer_size * (i + 1)
            # Send the remainder of the text, if there is any
            if(last_index != len(self.processed_text) - 1):
                text_buffer = self.processed_text[last_index:]
                client.send(text_buffer.encode('utf-8'))
            client.close()
            print("[x] Finished sending text to Android.")

            self.processed_text_lock.release()
        else:
            print("[ ] Could not aquire lock. Told client to wait.")
            message = "Image/text is being processed. Please wait."
            client.send(message.encode('utf-8'))
            client.close()

    def start_listening(self):
        """ Start loop to listen to the port specified in self.socket_port
        """
        self.__socket.listen(self.socket_backlog)
        print("[x] Starting loop to listen on port " + str(self.socket_port))
        while 1:
            try:
                # Try to receive and decode the incoming message
                client, address = self.__socket.accept()
                data = client.recv(self.socket_size)

                # Print instruction to console for debugging purposes
                print ("\n\n[x] Received INSTRUCTION: ", data.decode('utf-8'))

                if data.decode('utf-8') == "Send Image":
                    new_image_process_thread = Thread(target=self.process_image, args=(client))
                    new_image_process_thread.start()
                elif data.decode('utf-8') == "Send Text":
                    new_repace_proc_text_thread = Thread(target=self.replace_proc_text, args=(client))
                    new_repace_proc_text_thread.start()
                elif data.decode('utf-8') == "Receive Text"
                    new_send_proc_text_thread = Thread(target=self.send_proc_text, args=(client))
                    new_send_proc_text_thread.start()
            except:
                print("INSTRUCTION: FALSE")
                client.close()

##############################
######## USAGE SCRIPT ########
##############################
server = Central_Server()
server.start_listening()

""" END USAGE SCRIPT """
