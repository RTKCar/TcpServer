
from threading import Thread
from TcpServer import TcpServer
from PrintHandler import PrintHandler
from GuiHandler import GuiHandler
from MapAnalysis import MapAnalysis
from RoverHandler import RoverHandler
from RTKHandler import RTKHandler
from MessageHandler import MessageHandler

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
#parsed_JSON_obj = "[{\"conns\":[2,4],\"coord\":{\"lat\":56.67507440022754,\"long\":12.863477416073408},\"id\":1},{\"conns\":[1,3],\"coord\":{\"lat\":56.67501716123367,\"long\":12.862938208261255},\"id\":2},{\"conns\":[2,4],\"coord\":{\"lat\":56.67521716922783,\"long\":12.862889771317356},\"id\":3},{\"conns\":[3,1],\"coord\":{\"lat\":56.675154300977404,\"long\":12.863227111490545},\"id\":4}]"
#rover_position = ""
rover_position = (56.67515246104728,12.863372800241422)
map_analysis = ""
startSignal = False

def GUI():
    global GuiCon, GuiThread, map_analysis, parsed_JSON_obj, startSignal
    if not GuiCon.isRunning():
        if GuiThread.is_alive():
            GuiThread.join()
        GuiThread = Thread(target=GuiCon.start)
        GuiThread.start()
        while not GuiCon.isRunning():
            pass

    if GuiCon.isDataAvailable():
        data = GuiCon.getHandledData()
        print(data)
        if data[0] == 0:
            print(data[1])
            parsed_JSON_obj = data[1]
            map_analysis = MapAnalysis(parsed_JSON_obj)
        elif data[0] == 1 and len(rover_position) > 0 and parsed_JSON_obj and map_analysis:
            angle = map_analysis.Algo_peerPersuit(rover_position)
            RoverCon.send("START:" + str(int(angle)) + ";")
            startSignal = True
        elif data[0] == 2:
            startSignal = False
            RoverCon.send("STOP;")
        elif data[0] == 3:
            startSignal = False
            ret = data[1].split(';')
            for x in ret:
                if len(x) > 1:
                    RoverCon.send(x + ";")
        elif data[0] == 4:
            startSignal = False
            ret = data[1]
            RoverCon.send(ret)


def RTK():
    global rover_position, RTKThread
    if not RTKCon.isRunning():
        if RTKThread.isAlive():
            RTKThread.join()
        RTKThread = Thread(target=RTKCon.start)
        RTKThread.start()
        while not RTKCon.isRunning():
            pass
    if RTKCon.isDataAvailable():
        data = RTKCon.getHandledData()
        if data[0] == 0:
            rover_position = data[1]
            GuiCon.send("0:" + str(data[1][0]) + "," + str(data[1][1]) +
                        "," + str(data[2]) + ";")
            if startSignal:
                angle = map_analysis.Algo_peerPersuit(rover_position)
                RoverCon.send("START:" + str(int(angle)))

def Rover():
    global RoverThread
    if not RoverCon.isRunning():
        if RoverThread.is_alive():
            RoverThread.join()
        RoverThread = Thread(target=RoverCon.start)
        RoverThread.start()
        while not RoverCon.isRunning():
            pass
    #if RoverCon.isConnected():
    if RoverCon.isDataAvailable():
        data = RoverCon.getHandledData()
        if data:
            GuiCon.send(data)
    #elif RoverCon.get_first() and not RoverCon.isConnected():
    #    RoverCon.toggle_first(False)
    #    GuiCon.send('ROVER:DISCONNECTED')
    #    RTKCon.send('ROVER:DISCONNECTED')


try:
    while True:
        GUI()
        # RTK()
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

