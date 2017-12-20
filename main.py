
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler

testCon = TcpServer(9000, "Testing")
testCon.setAcceptAddress("0.0.0.0")
testCon.setMessageHandler(PrintHandler())
thread = Thread(target=testCon.start)
thread.start()


try:
    while thread.isAlive():
        pass
except KeyboardInterrupt as e:
    print(e)
    testCon.stop()
    thread.join()

