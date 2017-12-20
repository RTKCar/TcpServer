import MessageHandler
import json

class GuiHandler():
    def handle(self, data):
        if str(data).startswith("MAP;"):
            ret = self.JSON_parser(data)
            if ret:
                return (0, data)
            return (-1,"")
        elif str(data).startswith("START"):
            return (1, data)
        elif str(data).startswith("STOP"):
            return (2, data)

    def JSON_parser(self, JSON_obj):
        emptyString, split_JSON_obj, emptyShit = JSON_obj.split(';')
        if (len(split_JSON_obj) > 1):
            try:
                parsed_JSON_obj = json.loads(split_JSON_obj)
                return parsed_JSON_obj
                print ("parsing done")
                #self.print_JSON_obj()
            except Exception as e:
                print("Unexpected error: " + e)
        return False

"""
    def print_JSON_obj(self):
        print(self.parsed_JSON_obj[0].keys())
        print(type(self.parsed_JSON_obj[0]))
        for i in range(0, len(self.parsed_JSON_obj)):
            print(self.parsed_JSON_obj[i])
            print(
                "node ", self.parsed_JSON_obj[i]["id"], "has coordinates, lat: ", self.parsed_JSON_obj[i]["coord"]["lat"], " long: ",
                self.parsed_JSON_obj[i]["coord"]["long"], " and is connected to nodes ", self.parsed_JSON_obj[i]["conns"])
            print("Latitude: ", self.parsed_JSON_obj[i]["coord"]["lat"], "Longitude: ", self.parsed_JSON_obj[i]["coord"]["long"])
"""