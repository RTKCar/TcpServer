import pynmea2
from MessageHandler import MessageHandler

class RTKHandler(MessageHandler):

    def __init__(self):
        self.streamreader = pynmea2.NMEAStreamReader()


    #Returns a touple with (addData, response)
    def handle(self, data):
        for nmea_data in self.streamreader.next(data):
            if str(nmea_data).startswith('$GPGGA'):
                parse_msg = pynmea2.parse(str(nmea_data))
                fixed_status = parse_msg.data[4]
                #handled_data = "0:" + str(parse_msg.latitude) + ',' + str(parse_msg.longitude) + "," + str(fixed_status) + ";"
                #handled_data = str(parse_msg.latitude) + ',' + str(parse_msg.longitude)
                #print(handled_data)
                return (0, (parse_msg.latitude, parse_msg.longitude), fixed_status) #returnera
        return (-1, "")

