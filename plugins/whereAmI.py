#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on the WhereAmI plugins

import re
import urllib2, urllib
import json
import math
from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.mapObjects import SiriMapItemSnippet,SiriLocation, SiriMapItem
from siriObjects.systemObjects import GetRequestOrigin,Location

class location(Plugin):

    @register("de-DE", "(Wo bin ich.*)")    
    @register("en-US", "(Where am I.*)|(What is my location.*)")
    @register("zh-CN", u"(我在哪.*)|(我的位置.*)")
    @register("fr-FR", u'(Où suis-je.*)')
    def whereAmI(self, speech, language):
        mapGetLocation = self.getCurrentLocation()
        latitude = mapGetLocation.latitude
        longitude = mapGetLocation.longitude
        url = u"http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false&language={2}".format(str(latitude),str(longitude), language)
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            if response['status'] == 'OK':
                components = response['results'][0]['address_components']              
                street = filter(lambda x: True if "route" in x['types'] else False, components)[0]['long_name']
                stateLong= filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['long_name']
                try:
                    postalCode= filter(lambda x: True if "postal_code" in x['types'] else False, components)[0]['long_name']
                except:
                    postalCode=""
                try:
                    city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                except:
                    city=""
                countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                view = AddViews(self.refId, dialogPhase="Completion")
                if language == "de-DE":
                    the_header="Dein Standort"
                elif language == 'fr-FR':
                    the_header="Votre position"
                elif language == 'zh-CN':
                    self.say(u"这是您的位置 {0}：".format(self.user_name()))
                    the_header=u"您的位置"
                else:
                    self.say(u"This is your location {0}".format(self.user_name()))
                    the_header="Your location"
                Location=SiriLocation(the_header, street, city, stateLong, countryCode, postalCode, latitude, longitude)
                mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, Location)])
                view.views = [AssistantUtteranceView(text=the_header, dialogIdentifier="Map"), mapsnippet]
                self.sendRequestWithoutAnswer(view)
            else:
                if language=="de-DE":
                    self.say('Die Googlemaps informationen waren ungenügend!','Fehler')
                elif language == 'fr-FR':
                    self.say(u"La réponse de Googlemaps ne contient pas l'information nécessaire",'Erreur')
                elif language == 'zh-CN':
                    self.say(u"我无法在谷歌地图上找到所需信息。",u'错误')
                else:
                    self.say('The Googlemaps response did not hold the information i need!','Error')
        else:
            if language=="de-DE":
                self.say('Ich konnte keine Verbindung zu Googlemaps aufbauen','Fehler')
            if language=="fr-FR":
                self.say(u"Je ne peux pas établir de connexion à Googlemaps",'Erreur')
            if language=="zh-CN":
                self.say(u"我无法访问谷歌地图。", u'错误')
            else:
                self.say('Could not establish a conenction to Googlemaps','Error');
        self.complete_request()

    @register("de-DE", "(Wo liegt.*)")    
    @register("en-US", "(Where is.*)")
    @register("zh-CN", u"(.*在哪.*)")
    @register("fr-FR", u".*o(ù|u) (est |se trouve |ce trouve |se situe |ce situe )(.*)")
    def whereIs(self, speech, language, regex):
        the_location = None
        if language == "de-DE":
            the_location = re.match("(?u).* liegt ([\w ]+)$", speech, re.IGNORECASE)
            the_location = the_location.group(1).strip()
        elif language == 'fr-FR':
            the_location = regex.group(regex.lastindex).strip()
        elif language == 'zh-CN':
            the_location = re.match(u"(?u)([\w ]+)在哪.*", speech, re.IGNORECASE)
            the_location = the_location.group(1).strip()
        else:
            the_location = re.match("(?u).* is ([\w ]+)$", speech, re.IGNORECASE)
            the_location = the_location.group(1).strip()
        
        print the_location
        if the_location != None:
            the_location = the_location[0].upper()+the_location[1:]
        else:
            if language == "de-DE":
                self.say('Ich habe keinen Ort gefunden!',None)
            elif language == 'fr-FR':
                self.say(u"Désolé, je n'arrive pas à trouver cet endroit !")
            elif language == 'zh-CN':
                self.say(u"未找到位置。")
            else:
                self.say('No location found!',None)
            self.complete_request() 
            return
        url = u"http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false&language={1}".format(urllib.quote_plus(the_location.encode("utf-8")), language)
        jsonString=None
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            if response['status'] == 'OK':
                location = response['results'][0]['geometry']['location']
                city=response['results'][0]['address_components'][0]['long_name']
                try:
                    country=response['results'][0]['address_components'][2]['long_name']
                    countryCode=response['results'][0]['address_components'][2]['short_name']
                except:
                    country=the_location
                    countryCode=the_location
                if language=="de-DE":
                    the_header=u"Hier liegt {0}".format(the_location)
                elif language =="fr-FR":
                    the_header=u"Voici l'emplacement de {0} :".format(the_location)
                elif language =="zh-CN":
                    self.say(u"{0}在这里：".format(the_location))
                    the_header=u"{0}在这里：".format(the_location)
                else:
                    the_header=u"Here is {0}".format(the_location)
                view = AddViews(self.refId, dialogPhase="Completion")
                s_Location=Location(the_header, city, city, "", countryCode, "", str(location['lat']), str(location['lng']))
                mapsnippet = SiriMapItemSnippet(items=[SiriMapItem(the_header, s_Location, "BUSINESS_ITEM")])
                view.views = [AssistantUtteranceView(text=the_header, dialogIdentifier="Map"), mapsnippet]
                self.sendRequestWithoutAnswer(view)
            else:
                if language=="de-DE":
                    self.say('Die Googlemaps informationen waren ungenügend!','Fehler')
                elif language == "fr-FR":
                    self.say(u"Les informations demandées ne sont pas sur Google Maps !", u'Erreur')
                elif language == 'zh-CN':
                    self.say(u"我无法在谷歌地图上找到所需信息。",u'错误')
                else:
                    self.say('The Googlemaps response did not hold the information i need!','Error')
        else:
            if language=="de-DE":
                self.say('Ich konnte keine Verbindung zu Googlemaps aufbauen','Fehler')
            elif language == 'fr-FR':
                self.say(u"Je n'arrive pas à joindre Google Maps.", 'Erreur')
            elif language=="zh-CN":
                self.say(u"我无法访问谷歌地图。", u'错误')
            else:
                self.say('Could not establish a conenction to Google Maps.','Error');
        self.complete_request()        

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        RAD_PER_DEG = 0.017453293
        Rkm = 6371        
        dlon = lon2-lon1
        dlat = lat2-lat1
        dlon_rad = dlon*RAD_PER_DEG
        dlat_rad = dlat*RAD_PER_DEG
        lat1_rad = lat1*RAD_PER_DEG
        lon1_rad = lon1*RAD_PER_DEG
        lat2_rad = lat2*RAD_PER_DEG
        lon2_rad = lon2*RAD_PER_DEG
        
        a = (math.sin(dlat_rad/2))**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon_rad/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return round(Rkm * c,2)
