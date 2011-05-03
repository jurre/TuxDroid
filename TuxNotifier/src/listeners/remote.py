'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''
import time
import threading
import yaml

class RemoteListener(threading.Thread):

    """Constructor of remote, a remote object is created. 
    A tux and a runner object are added and the key-codes command are loaded."""
    def __init__(self, tux, runner):
        threading.Thread.__init__(self)
        self.tux = tux
        self.runner = runner
        self.comList = yaml.load(open("config/remote_config.yaml").read())
    
    """Start of the thread, the remote object constantly requests the state of the remote
    if the state is the same as the last state it is ignored because the program checks every 0.01 seconds.
    Humans press the buttons longer than that. Once a button is pressed it checks the comList for an command
    linkend to the key-code and puts that command in the runners commandlist"""    
    def run(self):
        self.run = True
        self.stateOld = ''
        while self.run == True:
            self.state = self.tux.tux.remote.getState()
            if self.state != self.stateOld:
                if self.state in self.comList:
                    self.runner.addCommand(self.comList[self.state])
           
            time.sleep(0.01)
            self.stateOld = self.state  
    
    """Set the run variable to False so the thread stops"""        
    def stop(self):
        self.run = False
