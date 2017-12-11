
from socket import *
from threading import Thread
from ReadHandler import ReadHandler
from WriteHandler import WriteHandler


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
        self.listenSocket.listen(3)
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
                    if(handledData[0]):
                        self.dataList.append(handledData[0])
                    if(handledData[1]):
                        self.sendBuffer.append(handledData[1])
        self.disconnect()


    def sendToGUI(self, data):
            self.sendBuffer.append(data)


    def send(self):
        while(self.running):
            for data in self.sendBuffer:
                self.clientSocket.send(data.encode('UTF-8'))
            self.sendBuffer = list()

    def receive(self):
        while(self.running):
            data = self.clientSocket.recv(1024).decode('UTF-8')
            if not data:
                self.running = False
                print("Client Dissconnected")
                return
            self.receiveBuffer.append(data)

    def getData(self):
        if self.dataList:
            return self.dataList.pop(0)
        return False


    def stop(self):
        self.running = False
        self.disconnect()

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


if __name__ == '__main__':

    rtkCon = TcpServer(2008)
    rtkCon.setAcceptAddress('0.0.0.0')
    rtkCon.setMessageHandler(WriteHandler())
    rtkThread = Thread(target=rtkCon.start)
    rtkThread.start()

    mapCon = TcpServer(2009)
    mapCon.setAcceptAddress('0.0.0.0')
    mapCon.setMessageHandler(ReadHandler())
    mapThread = Thread(target=mapCon.start)
    mapThread.start()

    while True:
        data = rtkCon.getData()
        if data:
            mapCon.sendToGUI(data)
        data = mapCon.getData()
        if data:
            if data.startswith('MAP'):
                print(data, " kolla denna boiii")


