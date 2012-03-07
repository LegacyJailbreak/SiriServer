#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *

class examplePlugin(Plugin):
    
    @register("de-DE", ".*Sinn.*Leben.*")
    @register("en-US", ".*Meaning.*Life.*")
    @register("zh-CN", ".*生.*意义.*")
    def meaningOfLife(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Willst du das wirklich wissen?")
            self.say(u"Du hast \"{0}\" gesagt!".format(answer))
        elif language == 'en-US':
            self.say("I shouldn't tell you!")
        elif language == 'zh-CN':
            self.say("这很难说。")
        self.complete_request()

    @register("de-DE", ".*standort.*test.*")
    @register("en-US", ".*location.*test.*")
    @register("zh-CN", ".*位置.*测试.*")
    def locationTest(self, speech, language):
        location = self.getCurrentLocation(force_reload=True)
        if language == 'zh-CN':
            self.say(u"纬度: {0}, 经度: {1}".format(location.latitude, location.longitude))
        else:
            self.say(u"lat: {0}, long: {1}".format(location.latitude, location.longitude))
        self.complete_request()