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
        self.commands = Queue.Queue()
        self.tux = TuxAPI(host, port)
        time.sleep(0.5)        
    
    def setListeners(self, listeners):
        self.listeners = listeners
    
    def setMessage(self, message):
        self.message = message
       
    def links(self):
        self.tux.spinning.leftOn(1.0, 5)
    
    def rechts(self):
        self.tux.spinning.rightOn(1.0, 5)
    
    def disconnect(self):
        self.tux.server.destroy()
        self.limit = 0
    
    def speak(self):        
        self.tux.mouth.open()
        self.tux.eyes.open()
        self.tux.tts.speak(self.message)    
        self.tux.mouth.open()
        self.tux.eyes.close()
        
    def stop(self):
        self.commands.put('stop')                   
    
    def listen(self):
        self.state = self.tux.remote.getState()
        if self.state == "K_LEFT":
            if(self.state != self.stateOld):                
                self.commands.put('left')
        if self.state == "K_1":
            if(self.state != self.stateOld):
                self.commands.put('ideal')
        if self.state == "K_2":
            if(self.state != self.stateOld):
                self.commands.put('live')
        if self.state == "K_3":
            if(self.state != self.stateOld):
                self.commands.put('independent')
        if self.state == "K_4":
            if(self.state != self.stateOld):
                self.commands.put('order')
        if self.state == "K_5":
            if(self.state != self.stateOld):
                self.commands.put('payment')
        if self.state == "K_6":
            if(self.state != self.stateOld):
                self.commands.put('test')
            
        if self.state == "K_RIGHT":                
            if(self.state != self.stateOld):
                self.commands.put('right')

        if self.state == "K_STANDBY":
            if(self.state != self.stateOld):                
                self.commands.put('stop')
                return

        if self.state == "K_OK":
                           
                self.commands.put('say')

        time.sleep(0.01)
        self.stateOld = self.state

    def connect(self):
        self.tux.server.connect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd") 
        #self.tux.tts.setLocutor("Sofie")