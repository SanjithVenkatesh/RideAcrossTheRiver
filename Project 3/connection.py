#Sanjith Venkatesh 20038520
#Project 3 Connection module:
#A module that interacts with the Open MapQuest APIs. This module builds URLs, makes HTTP requests, and parses JSON responses.

import json, urllib.request, urllib.parse

class Connection:

    BASE_URL = "http://open.mapquestapi.com/directions/v2/route?key=2S9ldXD1wdBUvPWccuGayKQSqbe47ZUv&ambiguities=ignore&"
    BASE_URL_ELEVATION = "http://open.mapquestapi.com/elevation/v1/profile?key=2S9ldXD1wdBUvPWccuGayKQSqbe47ZUv&callback=handleHelloWorldResponse&shapeFormat=raw&latLngCollection="

    #Builds the intial url for getting steps, total distance, total time, and latitude and longitude
    def build_url_for_request(self, locs: [list], outputs: [list]):
        urllist = []
        stufftoencode = []
        firstorsecond = 1
        for locs in locs:
            if firstorsecond == 1:
                stufftoencode.append(("from",locs))
                firstorsecond +=1
            else:
                stufftoencode.append(("to",locs))
        return Connection.BASE_URL+urllib.parse.urlencode(stufftoencode)
    
    #returns a list of latitude and longitude tuples that is needed for creating the elevation urls
    #The elevation api only takes urls with the longitude and latitude and not actual locations
    def getlatlonginfo(self,json_list):

        latlonglist = []
        for json in json_list['route']['locations']:
            lat = json['displayLatLng']['lat']
            long = json['displayLatLng']['lng']
            latlonglist.append((lat,long))
        return latlonglist

    #creates a list of urls for elevation api since it is easier to call for the elvation of each location than to put all the locations in one url
    #this way the 250 mile restriction can be ignored
    def getelevationurls(self,latlonglist):
        urllist = []
        for latlong in latlonglist:
            extrastuff = str(latlong[0])+","+str(latlong[1])
            urllist.append(Connection.BASE_URL_ELEVATION + extrastuff)
        return urllist

    def get_info(self, urls):
        response = None
        try:
            response = urllib.request.urlopen(urls)
            jsonstuff = response.read().decode('utf-8')
            # Elevation url returns json data inside of a string
            # Need to extract json data
            start = jsonstuff.find('{')
            end = jsonstuff.rfind('}')
            jsonstring = jsonstuff[start:end+1]
            json_text = json.loads(jsonstring)
            if json_text['info']['statuscode'] == 0: #checks if there is an error in the json data. If there is nothing wrong then statuscode is 0
                return json_text
            else:
                return None
        finally:
            if response != None:
                response.close()

    #Seperate function for getting the data for elevation since it requires seperate urls for each location
    #Each url then calls on the MapQuest and gets data that way
    #Function returns a list of json text that is ready to parse through like a dictionary
    def get_info_elevation(self,urllist):
        jsonlist = []
        for url in urllist:
            jsonlist.append(self.get_info(url))
        return jsonlist

    
    
           
           
           


                                                 
            
        
