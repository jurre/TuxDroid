'''
Created on May 2, 2011

@author: marthyn
'''
from Tux import *
from Runner import *    
from XmlListener import *

if __name__ == '__main__':
    myTux = Tux("127.0.0.1", 54321)
    myTux.connect()
    
    IdealListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Ideal/rssAll" ) 
    IndependentListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Independent/rssAll")
    LiveListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Live/rssAll")
    OrderListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Order/rssAll")
    PaymentListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Payment/rssAll")
    TestjobListener = XmlListener( myTux, "http://www.wtstest.com:8080/job/Test%20job/rssAll")
    listeners = {'ideal':IdealListener, 'independent':IndependentListener, 'live':LiveListener, 'order':OrderListener, 'payment':PaymentListener, 'test':TestjobListener}
    runner = Runner(myTux)
    runner.setListeners(listeners)
    runner.start()
    myTux.setListeners(listeners)
    for listener in listeners:
        listeners.get(listener).start()
    #IdealListener.start()
    #IndependentListener.start()
    #LiveListener.start()
    #OrderListener.start()
    #PaymentListener.start()
    
    myTux.listen()
    myTux.stop()