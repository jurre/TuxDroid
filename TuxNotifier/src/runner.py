'''
Created on May 2, 2011

@author: marthyn
'''
import threading
import Queue

class Runner( threading.Thread ):
    '''
    classdocs
    '''


    def __init__(self, tux):
        threading.Thread.__init__(self)
        self.commands = Queue.Queue()
        self.myTux = tux
    
    def setListeners(self, listeners):
        self.listeners = listeners
    
    def setRemote(self, remote):
        self.remote = remote
    
    def setText(self, text):
        self.text = text
    
    def run(self):
        while True:
            command = self.commands.get()
            if command == "stop":
                self.myTux.disconnect()
                for listener in self.listeners:
                    listener.stop()
                return
            if command == "say":
                self.myTux.speak(self.text)
            
            if self.listeners.has_key(command):
                self.listeners[command].getLastBuildStatus()
            
