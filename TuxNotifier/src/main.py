'''
Created on May 2, 2011

@author: marthyn
'''
from Tux import *
from Runner import *    
from XmlListener import *
from RemoteListener import *

if __name__ == '__main__':
    myTux = Tux("127.0.0.1", 54321)
    myTux.connect()
    
    runner = Runner(myTux)
    remote = RemoteListener(myTux, runner)
    
    
    IdealListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Ideal/rssAll" ) 
    IndependentListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Independent/rssAll")
    LiveListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Live/rssAll")
    OrderListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Order/rssAll")
    PaymentListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Payment/rssAll")
    TestjobListener = XmlListener( runner, "http://www.wtstest.com:8080/job/Test%20job/rssAll")
    listeners = {'ideal':IdealListener, 'independent':IndependentListener, 'live':LiveListener, 'order':OrderListener, 'payment':PaymentListener, 'test':TestjobListener}
    
    runner.setRemote(remote)
    runner.setListeners(listeners)
    remote.start()
    runner.start()
    
    for listener in listeners:
        listeners.get(listener).start()
