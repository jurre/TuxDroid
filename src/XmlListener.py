'''
Created on May 2, 2011

@author: marthyn
'''
import threading
import feedparser
import time
import re

class XmlListener(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, tux, url):
        threading.Thread.__init__(self)
        self.myTux = tux
        self.url=url
        
    def parse(self):
        self.feed = feedparser.parse( self.url )
    
    def run(self):
        self.run = "true"
        self.oldNumber = ""
        self.countFailures = 0
        while self.run == "true":
            self.parse()
            self.title = self.feed.entries[0].title            
            self.name = self.title.split('#')[0]
            self.number = self.title.split('#')[1].split(' ')[0]
            self.state = self.title.split('(')[1]          
            self.state = self.state.replace('(', '')
            self.state = self.state.replace(')', '')
            
            timestamp = self.feed.entries[0]['id']
            timestamp = timestamp[-19:]
            self.date = timestamp.split('_')[0]
            self.time = timestamp.split('_')[1].replace('-', ':')
            self.curString = "Name %s.\r Build#%s.\r State: %s.\r Date: %s.\r Time: %s." % (self.name, self.number, self.state, self.date, self.time)
            if self.number != self.oldNumber and self.oldNumber != "" :
                self.myTux.setMessage(str(self.curString))
                self.myTux.commands.put('say')
                print self.curString
                if 'broken' in self.state:
                    self.countFailures+=1
                    print self.countFailures  
            self.oldNumber = self.number          
            time.sleep(10)
            
    def stop(self):
        self.run = "false"
    
    def getLastBuildStatus(self):
        self.myTux.setMessage(str("Last build of job "+self.name+" was "+self.state))
        self.myTux.commands.put('say')
        
        
        