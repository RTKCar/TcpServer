
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler

RoverCon = TcpServer(9000, "Testing")
RoverCon.setAcceptAddress("0.0.0.0")
RoverCon.setMessageHandler(PrintHandler())
RoverThread = Thread()

RTKCon = TcpServer(9000, "Testing")
RTKCon.setAcceptAddress("0.0.0.0")
RTKCon.setMessageHandler(PrintHandler())
RTKThread = Thread()

GuiCon = TcpServer(9000, "Testing")
GuiCon.setAcceptAddress("0.0.0.0")
GuiCon.setMessageHandler(PrintHandler())
GuiThread = Thread()



def GUI()
    if not GuiCon.isRunning():
        if GuiThread.isAlive():
            GuiThread.join()
        GuiThread = Thread(target=testCon.start)
        GuiThread.start()

    data = ""
    if GuiCon.isDataAvailable():
        data = GuiCon.getHandledData()

    RTKCon.send(data)


def RTK()
    if not testCon.isRunning():
        if thread.isAlive():
            thread.join()
        thread = Thread(target=testCon.start)
        thread.start()

def Rover()
    pass



try:
    while True:

except KeyboardInterrupt as e:
    print(e)
    testCon.stop()
    thread.join()

