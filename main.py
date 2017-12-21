
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler
from GuiHandler import GuiHandler
from MapAnalysis import MapAnalysis
from RoverHandler import RoverHandler
from RTKHandler import RTKHandler

RoverCon = TcpServer(9001, "Rover")
RoverCon.setAcceptAddress("0.0.0.0")
RoverCon.setMessageHandler(RoverHandler())
RoverThread = Thread()

RTKCon = TcpServer(9002, "RTK")
RTKCon.setAcceptAddress("0.0.0.0")
RTKCon.setMessageHandler(RTKHandler())
RTKThread = Thread()

GuiCon = TcpServer(9003, "GUI")
GuiCon.setAcceptAddress("0.0.0.0")
GuiCon.setMessageHandler(GuiHandler())
GuiThread = Thread()

parsed_JSON_obj = ()
rover_position = ""
map_analysis = ""

def GUI():
    global GuiThread, map_analysis, parsed_JSON_obj
    if not GuiCon.isRunning():
        if GuiThread.is_alive():
            GuiThread.join()
        GuiThread = Thread(target=GuiCon.start)
        GuiThread.start()

    if GuiCon.isDataAvailable():
        data = GuiCon.getHandledData()
        print(data)
        if data[0] == 0:
            parsed_JSON_obj = data[1]
            map_analysis = MapAnalysis(parsed_JSON_obj)
        elif data[0] == 1 and len(rover_position) > 0 and parsed_JSON_obj and map_analysis:
            angle = map_analysis.Algo_peerPersuit(rover_position)
            RoverCon.send("0" + str(angle) + "," + data[1])
        elif data[0] == 2:
            RoverCon.send("1" + data[1])

def RTK():
    global rover_position
    if not RTKCon.isRunning():
        if RTKThread.isAlive():
            RTKThread.join()
        thread = Thread(target=RTKCon.start)
        thread.start()
    if RTKCon.isDataAvailable():
        data = RTKCon.getHandledData()
        if data[0] == 0:
            rover_position = data[1]
            GuiCon.send(data[1])

def Rover():
    if not RoverCon.isRunning():
        if RoverThread.is_alive():
            RoverThread.join()
        thread = Thread(target=RoverCon.start)
        thread.start()
    if RoverCon.isDataAvailable():
        data = RoverCon.getHandledData()
        if data:
            print(data)
            GuiCon.send(data)




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

