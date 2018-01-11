from MapAnalysis import MapAnalysis
import json
import time

def JSON_parser(JSON_obj):

    if (len(JSON_obj) > 1):
        try:
            parsed_JSON_obj = json.loads(JSON_obj)
            print(parsed_JSON_obj)
            return parsed_JSON_obj
            # self.print_JSON_obj()
        except Exception as e:
            print("Unexpected error: " + str(e))
    return False


rover_pos = ( 56.66323787096153 , 12.878742885738006 ), ( 56.66314061026385 , 12.878598891825959 ), ( 56.6631110964164 , 12.878471838914663 ), ( 56.66314656205318 , 12.878359630535101 ), ( 56.66320774191353 , 12.878317643820395 ), ( 56.66324122190209 , 12.878378623349533 ), ( 56.6633044214827 , 12.878480884787791 )
parsed_JSON_obj = "[{\"conns\":[2,4],\"coord\":{\"lat\":56.66329672972045,\"long\":12.878284881888675},\"id\":1},{\"conns\":[1,3],\"coord\":{\"lat\":56.66324094333677,\"long\":12.87838877294243},\"id\":2},{\"conns\":[2,4],\"coord\":{\"lat\":56.66335448141366,\"long\":12.878455855505564},\"id\":3},{\"conns\":[3,1],\"coord\":{\"lat\":56.66337026074343,\"long\":12.87833033757488},\"id\":4}]"
parsed_JSON_obj = JSON_parser(parsed_JSON_obj)
map_analysis = MapAnalysis(parsed_JSON_obj)



def my_run():
    global rover_pos, map_analysis
    for x in rover_pos:
        print(x)
    for x in rover_pos:
        map_analysis.Algo_peerPersuit(x)
        time.sleep(0.5)

if __name__ == '__main__':
    my_run()