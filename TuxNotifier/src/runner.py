'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''
import threading
import Queue
from action.speak import SpeakAction

class Runner( threading.Thread ):

    """Constructor of Runner, creates a runner object. A commandlist is added and a Tux object"""
    def __init__(self, tux):
        threading.Thread.__init__(self)
        self.commands = Queue.Queue()
        self.actions = Queue.Queue()     
        self.listeners = {}   
        self.tux = tux
    
    """Adds a listener"""
    def addListener(self, name, listener):
        if self.listeners.has_key(name):
            raise Exception('Listener with the same name already added: ' + name)
        else:
            self.listeners[name] = listener
    
    """Set the remote, so it can be used by runner, currently not used 8-) """
    def setRemote(self, remote):
        self.remote = remote
    
    def addCommand(self, command):
        self.commands.put(command)
        
    def addAction(self, command):
        print 'Runner::addAction "%s"' % command.__class__
        self.actions.put(command)
        self.commands.put('handleAction') # Dirty
    
    """The start of the thread and the main function. The runner handles the commands put in by other classes"""
    def run(self):
        print "Runner thread started"
    
        self.tux.openEyes()
        
        for name, listener in self.listeners.iteritems():
            print "Starting the thread of listener: " + name
            listener.start()
        
        while True:
            command = self.commands.get()
            
            if command == "stop":
                self.tux.disconnect()
                for listener in self.listeners:
                    listener.stop()
                return
                
            elif command == "handleAction":
                action = self.actions.get_nowait()
                action.setTux(self.tux)
                action.execute()
            
            elif self.listeners.has_key(command):
                lastBuildStatus = self.listeners[command].getLastBuildStatus()
                action = SpeakAction(lastBuildStatus)
                action.setTux(self.tux)                
                action.execute()
            
            self.commands.task_done()
