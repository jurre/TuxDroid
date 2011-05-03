'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''
import threading
import Queue

class Runner( threading.Thread ):

    """Constructor of Runner, creates a runner object. A commandlist is added and a Tux object"""
    def __init__(self, tux):
        threading.Thread.__init__(self)
        self.commands = Queue.Queue()
        self.myTux = tux
    
    """Set the listeners, so their functions can be used."""
    def setListeners(self, listeners):
        self.listeners = listeners
    
    """Set the remote, so it can be used by runner, currently not used 8-) """
    def setRemote(self, remote):
        self.remote = remote
    
    """Set the text that Tux will say if the say command is executed"""
    def setText(self, text):
        self.text = text
    
    """The start of the thread and the main function. The runner handles the commands put in by other classes"""
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
            
