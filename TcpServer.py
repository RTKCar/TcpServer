
from socket import *
from threading import Thread
from PrintHandler import PrintHandler


class TcpServer:
    def __init__(self, listenPort):
        self.serverPort = listenPort
        self.dataList = list()
        self.acceptAddress = 'localhost'

        self.running            = False
        self.receiveBuffer      = list()
        self.sendBuffer         = list()
        self.receivingThread    = Thread(target=self.receive)
        self.sendingThread      = Thread(target=self.send)


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
                handledData = self.messageHandler.handle(data)
                if(handledData):
                    if(handledData[1]):
                        self.dataList.append(handledData[1])
                    if(handledData[2]):
                        self.sendBuffer.append(handledData[2])

    def send(self):
        while(self.running):
            for data in self.sendBuffer:
                self.clientSocket.send(data.encode('UTF-8'))
            self.sendBuffer = list()

    def receive(self):
        while(self.running):
            data = self.clientSocket.recv(1024).decode('UTF-8')
            self.receiveBuffer.append(data)


    def getData(self):
        return dataList.pop(0)

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