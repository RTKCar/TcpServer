

from MessageHandler import MessageHandler

class PrintHandler(MessageHandler):
    def handle(self, data):
        print(data)
