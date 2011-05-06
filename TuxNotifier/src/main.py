'''
Created on May 2, 2011

@author: Marthyn Olthof, Daan Davidsz 
'''
import runner
import listeners.xml
import listeners.remote
import sys
from datetime import *
from action.speak import SpeakAction

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 54321
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    import tux.tux
    myTux = tux.tux.Tux(host, port)
    
    # Connect Tux object to the httpserver    
    myTux.connect()
    
    # Create a runner object
    runner = runner.Runner(myTux)
    
    # Create a remote object
    remote = listeners.remote.RemoteListener(myTux, runner)
    runner.setRemote(remote)
    remote.start()
    
    # Create xml listener object for every jenkins job
    idealListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Ideal/rssAll" ) 
    idealListener.setMinimumFailureCount(5)

    independentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Independent/rssAll")
    liveListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Live/rssAll")
    orderListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Order/rssAll")
    paymentListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Payment/rssAll")
    testjobListener = listeners.xml.XmlListener( runner, "http://www.wtstest.com:8080/job/Test%20job/rssAll")

    runner.addListener('ideal', idealListener)
    runner.addListener('independent', independentListener)
    runner.addListener('live', liveListener)
    runner.addListener('order', orderListener)
    runner.addListener('payment', paymentListener)    
    
    # Start the runner thread
    runner.start()
