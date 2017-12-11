

from MessageHandler import MessageHandler

class PrintHandler(MessageHandler):
    def handle(self, data):
        print("printing data inside TcpServer object: " + data)
        return (data, False)
