import sys
import time
import threading
import Queue

class FakeTuxRemote:

    def getState(self):
        return ''

class FakeTuxApi:

    def __init__(self, host, port):
        self.remote = FakeTuxRemote()

class Tux( threading.Thread ):

    def __init__(self, host, port):
        time.sleep(0.5)
        self.tux = FakeTuxApi(host, port)
        print "FakeTux: Initialized"

    def disconnect(self):
        pass
    
    def speak(self, text):        
        print 'FakeTux: Opening mouth'
        time.sleep(0.2)
        print 'FakeTux: Opening eyes'
        time.sleep(0.2)        
        print 'FakeTux: Speaking: "%s"' % text
        time.sleep(len(text) * 0.25)
        print 'FakeTux: Closing mouth'
        time.sleep(0.2)        
        print 'FakeTux: Closing eyes'                        
        time.sleep(0.2)        

    def connect(self):
        pass
