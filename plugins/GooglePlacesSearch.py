#!/usr/bin/python
# -*- coding: utf-8 -*-
# by Alex 'apexad' Martin
# help from: muhkuh0815 & gaVRos
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re
import urllib2, urllib
import json
import random
import math

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.systemObjects import GetRequestOrigin,Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.localsearchObjects import Business, MapItem, MapItemSnippet, Rating

googleplaces_api_key = APIKeyForAPI("google")
 
class googlePlacesSearch(Plugin):
     @register("en-US", "(find|show|where).* (nearest|nearby|closest) (.*)")
     @register("zh-CN", u"(找|告诉我|哪里|离我).*(近的|近|旁边的|旁边|周围的|周围)(.*)")
     @register("en-GB", "(find|show|where).* (nearest|nearby|closest) (.*)")
     def googleplaces_search(self, speech, language, regex):
          if language == "zh-CN":
              self.say(u'正在检索...', ' ')
          else:
              self.say('Searching...',' ')
          mapGetLocation = self.getCurrentLocation()
          latitude= mapGetLocation.latitude
          longitude= mapGetLocation.longitude
          Title = regex.group(regex.lastindex).strip()
          Query = urllib.quote_plus(str(Title.encode("utf-8")))
          random_results = random.randint(2,15)
          googleurl = "https://maps.googleapis.com/maps/api/place/search/json?location={0},{1}&radius=5000&keyword={2}&sensor=true&key={3}".format(latitude,longitude,str(Query),str(googleplaces_api_key))
          try:
               jsonString = urllib2.urlopen(googleurl, timeout=20).read()
          except:
               jsonString = None
          if jsonString != None:
               response = json.loads(jsonString)
               if (response['status'] == 'OK') and (len(response['results'])):
                    googleplaces_results = []
                    for result in response['results']:
                         if "rating" in result:
                              avg_rating = result["rating"]
                         else:
                              avg_rating = 0.0
                         rating = Rating(value=avg_rating, providerId='Google Places', count=0)
                         details = Business(totalNumberOfReviews=0,name=result['name'],rating=rating)
                         if (len(googleplaces_results) < random_results):
                              mapitem = MapItem(label=result['name'], street=result['vicinity'], latitude=result['geometry']['location']['lat'], longitude=result['geometry']['location']['lng'])
                              mapitem.detail = details
                              googleplaces_results.append(mapitem)
                         else:
                              break
                    mapsnippet = MapItemSnippet(items=googleplaces_results)
                    count_min = min(len(response['results']),random_results)
                    count_max = max(len(response['results']),random_results)
                    view = AddViews(self.refId, dialogPhase="Completion")
                    if language == "zh-CN":
                        view.views = [AssistantUtteranceView(speakableText=u'我找到'+str(count_max)+u'个有关'+str(Title.encode("utf-8"))+u'的结果。其中有'+str(count_min)+u'个离您很近：', dialogIdentifier="googlePlacesMap"), mapsnippet]
                    else:
                        view.views = [AssistantUtteranceView(speakableText='I found '+str(count_max)+' '+str(Title)+' results... '+str(count_min)+' of them are fairly close to you:', dialogIdentifier="googlePlacesMap"), mapsnippet]
                    self.sendRequestWithoutAnswer(view)
               else:
                    if language == "zh-CN":
                        self.say(u"抱歉，我找不到您附近有关"+str(Title.encode("utf-8"))+"的地点！")
                    else:
                        self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          else:
              if language == "zh-CN":
                  self.say(u"抱歉，我找不到您附近有关"+str(Title.encode("utf-8"))+"的地点！")
              else:
                  self.say("I'm sorry but I did not find any results for "+str(Title)+" near you!")
          self.complete_request()