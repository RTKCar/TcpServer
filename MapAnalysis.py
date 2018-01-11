import json
from math import radians, cos, sin, asin, sqrt, atan2
import math
from random import randint
import numpy
#from BaseStation import BaseStation

class MapAnalysis:

    prev_pos = [0.0, 0.0]

    def __init__(self, parsed_JSON_obj):
        self.init_process = True
        self.sub_state = False
        self.ClosestNode = -1
        self.PreviousNode = -1
        self.currentNode = dict()
        self.parsed_JSON_obj = parsed_JSON_obj

    def init_map(self):
        return self.init_process

    def sub_system_state(self, state):
        if state is True:
            self.sub_state = True
            return True


    def findClosestNode(self, RTK_point):
        dist = 9999999999.9
        index = -1
        for i in range(0, len(self.parsed_JSON_obj)):
            data1 = self.parsed_JSON_obj[i]["coord"]["lat"]
            data2 = self.parsed_JSON_obj[i]["coord"]["long"]
            tempTupple = (data1, data2)
            tempDist = self.getShortestDistance(RTK_point, tempTupple)
            if tempDist < dist:
                index = i
                dist = tempDist
        self.ClosestNode = index

    def getShortestDistance(self, RTK_point, ref_point):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(RTK_point[0])
        lon1 = radians(RTK_point[1])
        lat2 = radians(ref_point[0])
        lon2 = radians(ref_point[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        distance = distance * 100000
        return distance


    def getJsonIndex(self, jsonID):
        for i in range(0, len(self.parsed_JSON_obj)):
            if self.parsed_JSON_obj[i]["id"] == jsonID:
                return i
        return -1

    def JSON_parser(self, JSON_obj):
        #print(JSON_obj)
        #split_JSON_obj = JSON_obj.split(':')
        #print(split_JSON_obj)
        #emptyString, split_JSON_obj, emptyShit = JSON_obj.split(':')
        if (len(JSON_obj) > 1):
            try:
                parsed_JSON_obj = json.loads(JSON_obj)
                print(parsed_JSON_obj)
                return parsed_JSON_obj
                #self.print_JSON_obj()
            except Exception as e:
                print("Unexpected error: " + str(e))
        return False

    def Algo_peerPersuit(self, RTK_point):
        if self.init_process:
            self.init_process = False
            self.findClosestNode(RTK_point)
        if self.currentNode:
            #Check if RTK_point is close to point
            rtk_pos_tuple = (RTK_point[0], RTK_point[1])
            current_node_pos_tuple = (self.currentNode["coord"]["lat"], self.currentNode["coord"]["long"] )
            distance = self.getShortestDistance(rtk_pos_tuple, current_node_pos_tuple)

            if distance <= 100:
                self.PreviousNode = self.currentNode["id"]
                #Check for new point
                node = self.parsed_JSON_obj[self.nextNodeIndex()]
                self.currentNode = node
            else:
                #print ("if else")
                node = self.currentNode
        else:
            #print("else")
            node = self.parsed_JSON_obj[self.ClosestNode]
            self.currentNode = node
        data1 = node["coord"]["lat"]
        data2 = node["coord"]["long"]
        tempTuple = (data1, data2)
        return_data = self.getAngle(RTK_point, tempTuple)
        print(str(return_data) + "     " + str(self.currentNode["id"]))
        return return_data

    def nextNodeIndex(self):
        if self.PreviousNode is -1:
            return self.ClosestNode
        else:
            #Previous node != 1
            node = self.parsed_JSON_obj[self.getJsonIndex(self.PreviousNode)]
            #number = -1

            number = randint(0, len(node["conns"])-1)
            connection = node["conns"][number]
            index = self.getJsonIndex(connection)
            return index

    def getAngle(self, RTK_point, node_point): # Touple = (lat, lon)

        #pointB = (56.664420928659816, 12.878213831335472)
        if (type(RTK_point) != tuple) or (type(node_point) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(RTK_point[0])
        lat2 = math.radians(node_point[0])

        diffLong = math.radians(node_point[1] - RTK_point[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing) # rad * 180 / pi = deg
        #compass_bearing = (initial_bearing + 360) % 360
        #send_to_sub_unit = "10:" + str(compass_bearing) + ":0:0:0:0:0:0:0"

        #For Prev node

        lat1 = math.radians(self.prev_pos[0])
        lat2 = math.radians(RTK_point[0])

        diffLong = math.radians(RTK_point[1] - self.prev_pos[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

        initial_bearing_prev = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing_prev = math.degrees(initial_bearing_prev)
        #compass_bearing_prev = (initial_bearing + 360) % 360
        self.prev_pos[0] = RTK_point[0]
        self.prev_pos[1] = RTK_point[1]
        to_be_returned = initial_bearing - initial_bearing_prev
        return to_be_returned

    def testfunc(self, RTK_point):
        print("testFUNC")
        pointB = (56.664420928659816, 12.878213831335472)
        if (type(RTK_point) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(RTK_point[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - RTK_point[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        compass_bearing = int(compass_bearing)
        send_to_sub_unit = "10:" + str(compass_bearing) + ":0:0:0:0:0:0:0"
        return send_to_sub_unit