
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler

testCon = TcpServer(9000, "Testing")
testCon.setAcceptAddress("0.0.0.0")
testCon.setMessageHandler(PrintHandler())
thread = Thread()



try:
    while True:
        if not testCon.isRunning():
            if thread.isAlive():
                thread.join()
            thread = Thread(target=testCon.start)
            thread.start()
except KeyboardInterrupt as e:
    print(e)
    testCon.stop()
    thread.join()

