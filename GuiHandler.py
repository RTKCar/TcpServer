import MessageHandler
import json

class GuiHandler():
    def handle(self, data):
        if str(data).startswith("MAP"):

            return (0, data)
        elif str(data).startswith("START"):
            return (1, data)
        elif str(data).startswith("STOP"):
            return (2, data)

    def JSON_parser(self, JSON_obj):
        emptyString, split_JSON_obj, emptyShit = JSON_obj.split(';')
        if (len(split_JSON_obj) > 1):
            try:
                self.parsed_JSON_obj = json.loads(split_JSON_obj)
                self.init_process = True
                print ("parsing done")
                #self.print_JSON_obj()
            except Exception as e:
                print("Unexpected error: " + e)