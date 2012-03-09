#!/usr/bin/python
# -*- coding: utf-8 -*-

#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import os
from datetime import date
import locale 
from plugin import *

class talkToMe(Plugin):   
        
    @register("de-DE", ".*status.*")
    @register("en-US", ".*status.*")
    @register("zh-CN", u".*状态.*")
    def ttm_uptime_status(self, speech, language):
        uptime = os.popen("uptime").read()
        freemem = os.popen("grep MemFree /proc/meminfo").read()
        if language == 'de-DE':
            self.say('Hier ist der Status:')
            self.say(uptime, ' ')
            self.say(freemem, ' ')
        elif language == 'zh-CN':
            self.say(u'服务器状态：')
            self.say(uptime, u'这是运行时间。')
            self.say(freemem, u'这是剩余内存。')
        else:
            self.say('Here is the status:')
            self.say(uptime, 'This is running time.')
            self.say(freemem, 'And size of free memory.')
        self.complete_request()     
    
    
    @register("de-DE", "(Welcher Tag.*)|(Welches Datum.*)")
    @register("en-US", "(What Day.*)|(What.*Date.*)")
    
    def ttm_say_date(self, speech, language):
        now = date.today()
        if language == 'de-DE':
            locale.setlocale(locale.LC_ALL, 'de_DE')
            result=now.strftime("Heute ist %A, der %d.%m.%Y (Kalenderwoche: %W)")
            self.say(result)
        else:
            locale.setlocale(locale.LC_ALL, 'en_US')
            result=now.strftime("Today is %A the %d.%m.%Y (Week: %W)")
            self.say(result)
        self.complete_request()
