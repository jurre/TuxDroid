'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''

import sys
import time
from tuxisalive.api.TuxAPI import *
import threading
import Queue

class Tux( threading.Thread ):

    """Constructor of Tux, make a new TuxAPI object."""
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.tux = TuxAPI(host, port)
        time.sleep(0.5)        
    
    """Disconnect from the http-server."""
    def disconnect(self):
        self.tux.server.destroy()
        self.limit = 0
    
    """Tux open's his mouth and eyes and says the given text out loud."""
    def speak(self, text):        
        self.tux.mouth.open()
        self.tux.eyes.open()
        self.tux.tts.speak(text)    
        self.tux.mouth.open()
        self.tux.eyes.close()              
    
    """Connect to the http-server.""" 
    def connect(self):
        self.tux.server.connect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd") 
        #self.tux.tts.setLocutor("Sofie")
