

from MessageHandler import MessageHandler

class PrintHandler(MessageHandler):
    def handle(self, data):
        if not data:
            return
        print(data)
        return (data)

