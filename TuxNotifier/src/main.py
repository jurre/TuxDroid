'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz 
'''
import runner
import listeners.xml
import listeners.remote
import sys
from datetime import *

if __name__ == '__main__':

    """Create a tux or faketux, if the user has no actual TuxDroid and fake is added as argument
    the Tux object becomes a fake tux wich only prints out what Tux would do"""
    if len(sys.argv) > 1 and sys.argv[1] == 'fake':
        import tux.faketux
        myTux = tux.faketux.Tux("127.0.0.1", 54321)        
    else:
        import tux.tux
        myTux = tux.tux.Tux("127.0.0.1", 54321)
    
    #Connect Tux object to the httpserver    
    myTux.connect()
    #Create a runner object
    runner = runner.Runner(myTux)
    #Create a remote object
    remote = listeners.remote.RemoteListener(myTux, runner)
    
    #Create xml listener object for every jenkins job
    idealListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Ideal/rssAll" ) 
    independentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Independent/rssAll")
    liveListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Live/rssAll")
    orderListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Order/rssAll")
    paymentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Payment/rssAll")
    testjobListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Test%20job/rssAll")
    
    #Put the listeners in a map
    listeners = {'ideal': idealListener,
                 'independent': independentListener, 
                 'live': liveListener, 
                 'order': orderListener, 
                 'payment': paymentListener, 
                 'test': testjobListener}
    
    #Add the remote object to the runner object
    runner.setRemote(remote)
    #Add the listener objects to the runner object
    runner.setListeners(listeners)
    
    #Start the remote thread
    remote.start()
    #Start the runner thread
    runner.start()
    #Start the listener threads
    for listener in listeners:
        listeners.get(listener).start()
