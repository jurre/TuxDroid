'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz
'''
import threading
import feedparser
import time
from datetime import datetime
from action.speak import SpeakAction

class XmlListener(threading.Thread):

    """Constructor of XmlListener, creates a new Xmllistener object with the given url and adds a runner object"""
    def __init__(self, runner, url):
        threading.Thread.__init__(self)
        self.runner = runner
        self.url = url
        self.minimumFailureCount = 1
        
    def setMinimumFailureCount(self, count):
        self.minimumFailureCount = count
    
    """The start of the thread and main function. A continious loop checks the last entry of the RSS feed
    and checks if it is new and saves the name of the job, buildnumber, state, date and time."""
    def run(self):
        self.run = True
        self.oldNumber = False
        self.countFailures = 0
        self.brokeSinceTime = ""
        while self.run == True:
            self.checkBuildStatus()
            time.sleep(30) 
            
    def checkBuildStatus(self):
        try:
            print "Retrieving new status from URL: " + self.url
            feed = feedparser.parse( self.url )
            print "Retrieve succesful"
        except ex:
            print "Retrieve failed"
            message = "Could not retrieve the feed for job %s. Please help me." % self.name
            self.runner.addAction(SpeakAction(message))
            return
        
        self.title = feed.entries[0].title            
        self.name = self.title.split('#')[0]
        self.number = int(self.title.split('#')[1].split(' ')[0])
        self.state = self.title.split('(')[1].replace('(', '').replace(')', '')          
        timestamp = feed.entries[0]['id'][-19:]
        self.date = timestamp.split('_')[0]
        self.time = timestamp.split('_')[1].replace('-', ':')
        self.curString = "Name %s\nBuild # %s\nState: %s\nDate: %s\nTime: %s\n" % (self.name, self.number, self.state, self.date, self.time)
        
        if self.number != self.oldNumber:
            print self.curString #all new builds are printed

            if self.oldNumber != False:
                #If the build just broke, Tux tells us
                if 'broken since this build' in self.state: 
                    self.brokenSince = datetime.strptime(self.date + " " + self.time, "%Y-%m-%d %H:%M:%S")   
                    
                    if self.minimumFailureCount == 1:
                        self.runner.addAction(SpeakAction("Job %s broke. Please fix it!" % self.name))
                    elif self.countFailures >= self.minimumFailureCount:
                        self.runner.addAction(SpeakAction("Job %s has been broken for %s consecutive builds. Please fix it!" % (self.countFailures, self.name)))                  
                    
                #If the build was aborted, Tux lets us know
                if 'aborted' in self.state:
                    self.runner.addAction(SpeakAction("Job %s was aborted." % self.name))
                    
                #If the state is broken or broken since build ## then the failurecount is incremented
                if 'broken' in self.state:            
                    self.countFailures += 1
                    
                    #Every tenth consecutive broken build tux reminds us that it is broken. And how long ago it is
                    if self.countFailures % 10 == 0:
                        self.difference = str((datetime.now() - self.brokenSince))[:-7]
                        message = "Job %s is still broken. It has been broken for %s builds. In time that is %s" % (self.name, self.countFailures, self.difference)
                        self.runner.addAction(SpeakAction(message))
                        
                #If the state is stable again the counter is reset
                if 'back to normal' in self.state:
                    self.countFailures = 0
                    self.runner.addAction(SpeakAction("Job %s is back to normal again. Well done!" % self.name)) 
                        
        self.oldNumber = self.number  
            
    def stop(self):
        self.run = False
    
    def getLastBuildStatus(self):
        return "Last build job %s was %s" % (self.name, self.state)
