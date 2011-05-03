'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''
import threading
import feedparser
import time
import re
from datetime import datetime, timedelta

class XmlListener(threading.Thread):

    """Constructor of XmlListener, creates a new Xmllistener object with the given url and adds a runner object"""
    def __init__(self, runner, url):
        threading.Thread.__init__(self)
        self.runner = runner
        self.url = url
    
    """Parse the RSS feed"""    
    def parse(self):
        self.feed = feedparser.parse( self.url )
    
    """The start of the thread and main function. A continious loop checks the last entry of the RSS feed
    and checks if it is new and saves the name of the job, buildnumber, state, date and time."""
    def run(self):
        self.run = True
        self.oldNumber = False
        self.countFailures = int(0)
        self.brokeSinceTime = ""
        while self.run == True:
            self.parse() #This gets the newest feed from the url
            self.title = self.feed.entries[0].title            
            self.name = self.title.split('#')[0]
            self.number = int(self.title.split('#')[1].split(' ')[0])
            self.state = self.title.split('(')[1].replace('(', '').replace(')', '')          
            timestamp = self.feed.entries[0]['id'][-19:]
            self.date = timestamp.split('_')[0]
            self.time = timestamp.split('_')[1].replace('-', ':')
            self.curString = "Name %s.\rBuild # %s.\rState: %s.\rDate: %s.\rTime: %s.\n" % (self.name, self.number, self.state, self.date, self.time)
            if self.number != self.oldNumber:
                print self.curString #all new builds are printed

                if self.oldNumber != False:
                    #If the build just broke, Tux tells us
                    if 'broken since this build' in self.state: 
                        self.BrokenSince = datetime.strptime(self.date+" "+self.time, "%Y-%m-%d %H:%M:%S")   
                        self.runner.setText("Job %s broke. Please fix it!" % (self.name)) 
                        self.runner.commands.put('say')
                        
                    #If the build was aborted, Tux let's us know
                    if 'aborted' in self.state:
                        self.runner.setText("Job %s was aborted." % (self.name)) 
                        self.runner.commands.put('say')
                    #If the state is broken or broken since build ## then the failurecount is incremented
                    if 'broken' in self.state:            
                        self.countFailures+=1
                        
                        #Every tenth consecutive broken build tux reminds us that it is broken. And how long ago it is
                        if self.countFailures%10 == 0:
                            self.difference = str((datetime.now() - self.BrokenSince))[:-7]      
                            self.runner.setText("Job %s is still broken. It has been broken for %s builds. In time that is %s" % (self.name, self.countFailures, self.difference)) 
                            self.runner.commands.put('say')
                    #If the state is stable again the counter is reset
                    if 'back to normal' in self.state:
                        self.countFailures= 0
                        self.runner.setText("Job %s is back to normal again. Well done!" % (self.name)) 
                        self.runner.commands.put('say')
                    
                    
                            
            self.oldNumber = self.number           
            time.sleep(30) 
            
    def stop(self):
        self.run = False
    
    def getLastBuildStatus(self):
        self.runner.setText("Last build job %s was %s" % (self.name, self.state))
        print self.curString
        self.runner.commands.put('say')
