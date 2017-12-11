
from socket import *
from threading import Thread
from PrintHandler import PrintHandler


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


#TODO fix timeout for listening for connections
    def connect(self):
        print("Waiting for connection")
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        self.listenSocket.bind((self.acceptAddress, self.serverPort))
        self.listenSocket.listen(1)
        (self.clientSocket, self.clientAddress) = self.listenSocket.accept()
        self.listenSocket.close()
        print("Connection established - Client: " + str(self.clientAddress))


#TODO fix disconnect, client needs to know server is disconnecting
    def disconnect(self):
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
                if(handledData):
                    if(handledData[0]):
                        self.handledData.append(handledData[0])
                    if(handledData[1]):
                        self.sendBuffer.append(handledData[1])

    #Loop for sending thread
    def sendingLoop(self):
        while(self.running):
            for data in self.sendBuffer:
                try:
                    self.clientSocket.sendingLoop(data.encode('UTF-8'))
                except Exception:
                    self.running = False
                    self.sendBuffer = list()
                    return
            self.sendBuffer = list()

    #Loop for receiving thread
    def receivingLoop(self):
        while(self.running):
            data = self.clientSocket.recv(1024).decode('UTF-8')
                if not data:
                    self.running = False;
                    return
            self.receiveBuffer.append(data)

    #Method to be able to send data from outside class outside
    def send(self, data):
        self.sendBuffer.append(data);

    # get data handled with defined messagehandler
    def getHandledData(self):
        if(self.handledData):
            return self.handledData.pop(0)
        return False

    def stop(self):
        self.running = False
        disconnect()

    def start(self):
        self.connect()
        self.running = True
        print("Starting sending thread")
        self.sendingThread.start()
        print("Starting receiving thread")
        self.receivingThread.start()
        self.run()

    def setMessageHandler(self, messageHandler):
        self.messageHandler = messageHandler


con = TcpServer(9000)
con.setAcceptAddress('0.0.0.0')
con.setMessageHandler(PrintHandler())
con.start()