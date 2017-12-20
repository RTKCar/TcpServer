
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler
from GuiHandler import GuiHandler

RoverCon = TcpServer(9001, "Rover")
RoverCon.setAcceptAddress("0.0.0.0")
RoverCon.setMessageHandler(PrintHandler())
RoverThread = Thread()

RTKCon = TcpServer(9002, "RTK")
RTKCon.setAcceptAddress("0.0.0.0")
RTKCon.setMessageHandler(PrintHandler())
RTKThread = Thread()

GuiCon = TcpServer(9003, "GUI")
GuiCon.setAcceptAddress("0.0.0.0")
GuiCon.setMessageHandler(GuiHandler())
GuiThread = Thread()



def GUI():
    global GuiThread
    if not GuiCon.isRunning():
        if GuiThread.is_alive():
            GuiThread.join()
        GuiThread = Thread(target=GuiCon.start)
        GuiThread.start()

    data = ""
    if GuiCon.isDataAvailable():
        data = GuiCon.getHandledData()
        print(data)


def RTK():
    if not RTKCon.isRunning():
        if RTKThread.isAlive():
            RTKThread.join()
        thread = Thread(target=RTKCon.start)
        thread.start()

def Rover():
    if not RoverCon.isRunning():
        if RoverThread.is_alive():
            RoverThread.join()
        thread = Thread(target=RoverCon.start)
        thread.start()



try:
    while True:
        GUI()
        RTK()
        Rover()
except KeyboardInterrupt as e:
    print(e)
    print("Stopping")
    GuiCon.stopServer()
   # if GuiThread.isAlive():
   #     GuiThread.join()
    RTKCon.stopServer()
   # if RTKThread.isAlive():
   #     RTKThread.join()
    RoverCon.stopServer()
  #  if RoverThread.isAlive():
  #      RoverThread.join()
    print("wtf")

