'''
Created on May 2, 2011

@author: marthyn
'''
import threading

class Runner( threading.Thread ):
    '''
    classdocs
    '''


    def __init__(self, tux):
        threading.Thread.__init__(self)
        self.myTux = tux
    
    def setListeners(self, listeners):
        self.listeners = listeners
            
    def run(self):
        while True:
            command = self.myTux.commands.get()
            if command == "stop":
                self.myTux.disconnect()
                for listener in self.listeners:
                    listener.stop()
                return
            if command == "left":
                self.myTux.links()
            if command == "right":
                self.myTux.rechts()
            if command == "say":
                self.myTux.speak()
            
            if self.listeners.has_key(command):
                self.listeners[command].getLastBuildStatus()
            
            print command