from socket import *
from threading import Thread
from MessageHandler import MessageHandler
import datetime


class TcpServer:
    def __init__(self, listenport, identifier=""):
        self.serverPort = listenport
        self.acceptAddress = 'localhost'
        self.id = identifier
        self.running = False
        self.connected = False
        self.handledData = list()
        self.receiveBuffer = list()
        self.sendBuffer = list()
        self.receivingThread = Thread(target=self.receivingLoop)
        self.sendingThread = Thread(target=self.sendingLoop)

        self.messageHandler = MessageHandler()

        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        self.listenSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.first = True
        self.clientSocket = None
        self.clientAddress = None

    def reset(self):
        print("[" + self.id + "] Resetting")
        if self.running:
            self.stop()
        self.running = False
        self.connected = False
        self.handledData.clear()
        self.receiveBuffer.clear()
        self.sendBuffer.clear()
        self.receivingThread = Thread(target=self.receivingLoop)
        self.sendingThread = Thread(target=self.sendingLoop)
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        self.listenSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # open a listening socket on set port to listen for client connections
    def connect(self):
        print("[" + self.id + "] Waiting for connection")

        try:
            self.listenSocket.bind((self.acceptAddress, self.serverPort))
            self.listenSocket.listen(1)
        except OSError as e:
            print(e)
            self.disconnect()
            return False
        try:
            (self.clientSocket, self.clientAddress) = self.listenSocket.accept()
        except Exception as e:
            print("[" + self.id + "]" + str(e) + " Stopped listening")
            self.disconnect()
            return False
        self.listenSocket.shutdown(SHUT_RDWR)
        self.listenSocket.close()
        print("[" + self.id + "] Connection established - Client: " + str(self.clientAddress))
        self.connected = True
        return True

    def isRunning(self):
        return self.running

    def isConnected(self):
        return self.connected

# TODO fix disconnect, client needs to know server is disconnecting
    def disconnect(self):
        try:
            self.clientSocket.shutdown(SHUT_RDWR)
        except Exception as e:
            print("["+self.id+"]"+str(e))
        try:
            self.clientSocket.close()
        except Exception as e:
            print("["+self.id+"]"+str(e))
        try:
            self.listenSocket.shutdown(SHUT_RDWR)
        except Exception as e:
            print("["+self.id+"]"+str(e))
        try:
            self.listenSocket.close()
        except Exception as e:
            print("["+self.id+"]"+str(e))
        self.connected = False

    # set which IP addresses the server accepts
    def setAcceptAddress(self, ip):
        self.acceptAddress = ip

    # set which port the server listens on
    def setServerPort(self, port):
        self.serverPort = port

    # main server loop
    def run(self):
        while self.running:
            if self.receiveBuffer:
                data = self.receiveBuffer.pop(0)
                handledData = self.messageHandler.handle(data)  # Returns touple with (handledData, response to client)
                if handledData:
                    self.handledData.append(handledData)
        self.stop()

    # Loop for sending thread
    def sendingLoop(self):
        while self.running:
            if self.sendBuffer:
                try:
                    data = self.sendBuffer.pop(0)
                    #print("Data start send by server: " + str(data) + " " + str(datetime.datetime.now()))
                    self.clientSocket.send(data.encode('UTF-8'))
                    #print("Data done send by server: " + str(data) + " " + str(datetime.datetime.now()))
                except Exception as e:
                    print(e)
                    self.running = False
                    self.sendBuffer = list()

    # Loop for receiving thread
    def receivingLoop(self):
        while self.running:
            try:
                data = self.clientSocket.recv(1024).decode('UTF-8')
                #print("Data done received by server: " + str(data) + " " + str(datetime.datetime.now()))
                if not data:
                    self.running = False
                else:
                    self.receiveBuffer.append(data)
            except ConnectionAbortedError:
                self.running = False
            except Exception as e:
                print(e)
                self.running = False

    # Method to be able to send data from outside class outside
    def send(self, data):
        self.sendBuffer.append(data)

    # get data handled with defined messagehandler
    def getHandledData(self):
        if self.handledData:
            return self.handledData.pop(0)
        return False

    # check if server has received data
    def isDataAvailable(self):
        if self.handledData:
            return True
        return False

    def stopServer(self):
        self.running = False
        self.disconnect()

    # stops the server
    def stop(self):
        self.disconnect()
        if self.sendingThread.isAlive():
            self.sendingThread.join()
        if self.receivingThread.isAlive():
            self.receivingThread.join()
        print("[" + self.id + "] Disconnected and stopped")

    # starts server
    def start(self):
        self.reset()
        self.running = True
        self.connect()

        if self.isConnected():
            self.sendingThread.start()
            self.receivingThread.start()
            self.run()
        self.running = False

    def setMessageHandler(self, messageHandler):
        self.messageHandler = messageHandler
