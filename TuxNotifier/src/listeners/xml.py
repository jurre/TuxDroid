'''
Created on May 2, 2011

@author: marthyn
'''
import threading
import feedparser
import time
import re

class XmlListener(threading.Thread):

    def __init__(self, runner, url):
        threading.Thread.__init__(self)
        self.runner = runner
        self.url = url
        
    def parse(self):
        self.feed = feedparser.parse( self.url )
    
    def run(self):
        self.run = True
        self.oldNumber = False
        self.countFailures = 0
        while self.run == True:
            self.parse()
            self.title = self.feed.entries[0].title            
            self.name = self.title.split('#')[0]
            self.number = int(self.title.split('#')[1].split(' ')[0])
            self.state = self.title.split('(')[1]          
            self.state = self.state.replace('(', '')
            self.state = self.state.replace(')', '')
            
            timestamp = self.feed.entries[0]['id']
            timestamp = timestamp[-19:]
            self.date = timestamp.split('_')[0]
            self.time = timestamp.split('_')[1].replace('-', ':')
            self.curString = "Name %s.\rBuild # %s.\rState: %s.\rDate: %s.\rTime: %s.\n" % (self.name, self.number, self.state, self.date, self.time)
            if self.number != self.oldNumber:
                print self.curString
            if self.number != self.oldNumber and self.oldNumber != False and self.state != 'stable':
                self.runner.setText("Status of build # %s of job %s is %s" % (self.number, self.name, self.state))
                self.runner.commands.put('say')
                
                if 'broken' in self.state:
                    self.countFailures+=1
                    print self.countFailures  
            self.oldNumber = self.number          
            time.sleep(10)
            
    def stop(self):
        self.run = False
    
    def getLastBuildStatus(self):
        self.runner.setText("Last build of %s test was %s" % (self.name, self.state))
        print self.curString
        self.runner.commands.put('say')
