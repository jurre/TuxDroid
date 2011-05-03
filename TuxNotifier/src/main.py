'''
Created on May 2, 2011

@author: marthyn
'''
import runner
import listeners.xml
import listeners.remote
import sys

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'fake':
        import tux.faketux
        myTux = tux.faketux.Tux("127.0.0.1", 54321)        
    else:
        import tux.tux
        myTux = tux.tux.Tux("127.0.0.1", 54321)
        
    myTux.connect()
    
    runner = runner.Runner(myTux)
    remote = listeners.remote.RemoteListener(myTux, runner)
    
    idealListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Ideal/rssAll" ) 
    independentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Independent/rssAll")
    liveListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Live/rssAll")
    orderListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Order/rssAll")
    paymentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Payment/rssAll")
    testjobListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Test%20job/rssAll")
    
    listeners = {'ideal': idealListener,
                 'independent': independentListener, 
                 'live': liveListener, 
                 'order': orderListener, 
                 'payment': paymentListener, 
                 'test': testjobListener}
    
    runner.setRemote(remote)
    runner.setListeners(listeners)
    remote.start()
    runner.start()
    
    for listener in listeners:
        listeners.get(listener).start()
