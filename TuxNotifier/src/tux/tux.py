'''
Created on May 2, 2011

@author: marthyn
'''

import sys
import time
from tuxisalive.api.TuxAPI import *
import threading
import Queue

class Tux( threading.Thread ):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.tux = TuxAPI(host, port)
        time.sleep(0.5)        

    def disconnect(self):
        self.tux.server.destroy()
        self.limit = 0
    
    def speak(self, text):        
        self.tux.mouth.open()
        self.tux.eyes.open()
        self.tux.tts.speak(text)    
        self.tux.mouth.open()
        self.tux.eyes.close()              

    def connect(self):
        self.tux.server.connect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd") 
        #self.tux.tts.setLocutor("Sofie")
