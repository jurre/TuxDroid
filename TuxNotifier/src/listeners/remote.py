'''
Created on May 2, 2011

@author: marthyn
'''
import time
import threading
import yaml

class RemoteListener(threading.Thread):

    def __init__(self, tux, runner):
        threading.Thread.__init__(self)
        self.tux = tux
        self.runner = runner
        self.comList = yaml.load(open("config/remote_config.yaml").read())
        
    def run(self):
        self.run = True
        self.stateOld = ''
        while self.run == True:
            self.state = self.tux.tux.remote.getState()
            if self.state != self.stateOld:
                if self.state in self.comList:
                    self.runner.commands.put(self.comList[self.state])
           
            time.sleep(0.01)
            self.stateOld = self.state  
            
    def stop(self):
        self.run = False
