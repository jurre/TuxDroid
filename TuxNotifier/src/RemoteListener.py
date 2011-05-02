'''
Created on May 2, 2011

@author: marthyn
'''
import time
import threading
class RemoteListener(threading.Thread):

    def __init__(self, tux, runner):
        threading.Thread.__init__(self)
        self.tux = tux
        self.runner = runner
        self.comList = {"K_1":"ideal", "K_2":"live", "K_3":"independent", "K_4":"order", "K_5":"payment", "K_6":"test", "K_STANDBY":"stop"}
        
        
    def run(self):
        self.run = 'true'
        self.stateOld = ''
        while self.run=='true':
            self.state = self.tux.tux.remote.getState()
            if self.state != self.stateOld:
                if self.state in self.comList:
                    self.runner.commands.put(self.comList[self.state])
           
            time.sleep(0.01)
            self.stateOld = self.state  
            
    def stop(self):
        self.run = 'false'