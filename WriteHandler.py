import pynmea2
from MessageHandler import MessageHandler

class WriteHandler(MessageHandler):

    def __init__(self):
        self.streamreader = pynmea2.NMEAStreamReader()

    #Returns a touple with (addData, response)
    def handle(self, data):

        for nmea_data in self.streamreader.next(data):
            if str(nmea_data).startswith('$GPGGA'):
                parse_msg = pynmea2.parse(str(nmea_data))
                data_to_send = str(parse_msg.latitude) + ',' + str(parse_msg.longitude) + ',' + str(parse_msg.altitude)
                return (data_to_send, False) #returnera
        return False
