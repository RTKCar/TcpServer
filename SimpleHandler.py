from MessageHandler import MessageHandler

class SimpleHandler(MessageHandler):
    def handle(self, data):
        return (data, False)
