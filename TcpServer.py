
from socket import *
from threading import Thread


class TcpServer:
    def __init__(self, listenPort, identifier=""):
        self.serverPort = listenPort
        self.acceptAddress = 'localhost'
        self.id = identifier
        self.running = False



    def reset(self):
        print("[" + self.id + "] Resetting")
        if self.running:
            self.stop()
        self.running= False
        self.handledData = list()
        self.receiveBuffer = list()
        self.sendBuffer = list()
        self.receivingThread = Thread(target=self.receivingLoop)
        self.sendingThread = Thread(target=self.sendingLoop)

    #open a listening socket on set port to listen for client connections
    def connect(self):
        print("[" + self.id + "] Waiting for connection")
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        self.listenSocket.bind((self.acceptAddress, self.serverPort))
        self.listenSocket.listen(1)
        try:
            (self.clientSocket, self.clientAddress) = self.listenSocket.accept()
        except Exception as e:
            print(e)
            self.listenSocket.close()
            return
        self.listenSocket.close()
        print("[" + self.id +"] Connection established - Client: " + str(self.clientAddress))
        self.connected = True

    def isRunning(self):
        return self.running

    def isConnected(self):
        return self.connected

#TODO fix disconnect, client needs to know server is disconnecting
    def disconnect(self):
        if self.isConnected():
            self.clientSocket.close()
        else:
            self.listenSocket.close()
        self.connected = False

    #set which IP addresses the server accepts
    def setAcceptAddress(self, ip):
        self.acceptAddress = ip

    #set which port the server listens on
    def setServerPort(self, port):
        self.serverPort = port

    #main server loop
    def run(self):
        while(self.running):
            if(self.receiveBuffer):
                data = self.receiveBuffer.pop(0)
                handledData = self.messageHandler.handle(data) #Returns touple with (handledData, response to client)
                if handledData:
                    if(handledData[0]):
                        self.handledData.append(handledData[0])
                    if(handledData[1]):
                        self.sendBuffer.append(handledData[1])
        self.stop()

    #Loop for sending thread
    def sendingLoop(self):
        while(self.running):
            for data in self.sendBuffer:
                try:
                    self.clientSocket.send(data.encode('UTF-8'))
                except Exception as e:
                    print(e)
                    self.running = False
                    self.sendBuffer = list()
                    print("[" + self.id + "] Sendingloop stopping")
                    return
            self.sendBuffer = list()
        print("[" + self.id + "] Sendingloop stopping")

    #Loop for receiving thread
    def receivingLoop(self):
        while(self.running):
            try:
                data = self.clientSocket.recv(1024).decode('UTF-8')
                if not data:
                    self.running = False
            except ConnectionAbortedError:
                return
            except timeout:
                pass
                return
            self.receiveBuffer.append(data)
        print("[" + self.id + "] Receivingloop stopping")

    #Method to be able to send data from outside class outside
    def send(self, data):
        self.sendBuffer.append(data)

    # get data handled with defined messagehandler
    def getHandledData(self):
        if(self.handledData):
            return self.handledData.pop(0)
        return False

    #check if server has received data
    def isDataAvailable(self):
        if(self.handledData):
            return True
        return False

    #stops the server
    def stop(self):
        print("["+ self.id + "] Stopping server")
        self.disconnect()
        if self.sendingThread.isAlive():
            print("["+ self.id + "] Waiting for sendingthread")
            self.sendingThread.join()
        if self.receivingThread.isAlive():
            print("["+ self.id + "] Waiting for receivingthread")
            self.receivingThread.join()
        print("["+ self.id + "] Disconnected and stopped")
        self.running = False


    #starts server
    def start(self):
        self.reset()
        self.running = True
        self.connect()

        if(self.isConnected()):
            print("[" + self.id + "] Starting sending thread")
            self.sendingThread.start()
            print("[" + self.id + "] Starting receiving thread")
            self.receivingThread.start()
            self.run()
        self.running = False
    def setMessageHandler(self, messageHandler):
        self.messageHandler = messageHandler
