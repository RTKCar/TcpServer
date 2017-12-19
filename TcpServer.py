
from socket import *
from threading import Thread
from PrintHandler import PrintHandler
from MessageHandler import MessageHandler
from NmeaHandler import NmeaHandler
from sys import getsizeof


class TcpServer:
    def __init__(self, listenPort):
        self.serverPort = listenPort
        self.handledData = list()
        self.acceptAddress = 'localhost'

        self.running            = False
        self.receiveBuffer      = list()
        self.sendBuffer         = list()
        self.receivingThread    = Thread(target=self.receivingLoop)
        self.sendingThread      = Thread(target=self.sendingLoop)
        self.connected = False



#TODO fix timeout for listening for connections
    def connect(self):
        print("Waiting for connection")
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.listenSocket.bind((self.acceptAddress, self.serverPort))
        except Exception as e:
            print(e)
            self.listenSocket.close()
            return
        self.listenSocket.listen(1)
        (self.clientSocket, self.clientAddress) = self.listenSocket.accept()
        self.listenSocket.close()
        #self.clientSocket.settimeout(1)
        print("Connection established - Client: " + str(self.clientAddress))
        self.connected = True

    def isConnected(self):
        return self.connected

#TODO fix disconnect, client needs to know server is disconnecting
    def disconnect(self):
        if self.isConnected():
            self.clientSocket.close()

    def setAcceptAddress(self, ip):
        self.acceptAddress = ip

    def setServerPort(self, port):
        self.serverPort = port

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
        #self.disconnect()

    #Loop for sending thread
    def sendingLoop(self):
        while(self.running):
            for data in self.sendBuffer:
                try:
                    print("Sending data: ---" + str(getsizeof(data)) + "---" + data)
                    self.clientSocket.send(data.encode('UTF-8'))
                except Exception as e:
                    print(e)
                    self.running = False
                    self.sendBuffer = list()
                    return
            self.sendBuffer = list()

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

    #Method to be able to send data from outside class outside
    def send(self, data):
        self.sendBuffer.append(data)

    # get data handled with defined messagehandler
    def getHandledData(self):
        if(self.handledData):
            return self.handledData.pop(0)
        return False

    def isDataAvailable(self):
        if(self.handledData):
            return True
        return False

    def stop(self):
        self.running = False

        print("Stopping")
        self.disconnect()
        if self.sendingThread.isAlive():
            print("Waiting for sendingthread")
            self.sendingThread.join()
        if self.receivingThread.isAlive():
            print("Waiting for receivingthread")
            self.receivingThread.join()
        print("Disconnected and stopped")
        self.connected = False

    def start(self):
        self.connect()
        if(self.isConnected()):
            self.running = True
            print("Starting sending thread")
            self.sendingThread.start()
            print("Starting receiving thread")
            self.receivingThread.start()
            self.run()

    def setMessageHandler(self, messageHandler):
        self.messageHandler = messageHandler
