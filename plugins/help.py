#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna thanks for help to john-dev

import re,os

config_file="plugins.conf"
pluginPath="plugins"
from plugin import *
tline_answer_de = ''
tline_answer_en = ''
tline_answer_zh = ''

with open(config_file, "r") as fh:
    for line in fh:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue
        try:
            with open(pluginPath+"/"+line+".py", "r") as fd:
                for tline in fd:
                    tline=tline.strip()
                    if tline.startswith("@register(\"de-DE\", "):
                        tline = tline.replace('@register','').replace('(','').replace(')','').replace('\"','').replace('.','').replace('de-DE, ','').replace('[a-zA-Z0-9]+','').replace('\w','').replace('|',' oder ').replace('*',' ').replace('>',' ').replace('?',' ').replace('<',' ')
                        tline_answer_de = tline_answer_de +'\n' + "".join(tline)
                    
                    elif tline.startswith("@register(\"en-US\", "):
                        tline = tline.replace('@register','').replace('(','').replace(')','').replace('\"','').replace('.','').replace('en-US, ','').replace('[a-zA-Z0-9]+','').replace('\w','').replace('|',' or  ')
                        tline_answer_en = tline_answer_en +'\n' + "".join(tline)
                        
                    elif tline.startswith("@register(\"zh-CN\", "):
                        tline = tline.replace('@register','').replace('(','').replace(')','').replace('\"','').replace('.','').replace('zh-CN, ','').replace('[a-zA-Z0-9]+','').replace('\w','').replace('|',' or  ')
                        tline_answer_zh = tline_answer_zh +'\n' + "".join(tline)
        
        except:
            tline = "Plugin loading failed"

class help(Plugin):
    
    @register("de-DE", "(Hilfe)|(Befehle)")
    @register("en-US", "(Help)|(Commands)")
    @register("zh-CN", u"(帮助)|(命令)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say(u"Das sind die Befehle die in Deiner Sprache verfügbar sind:")
            self.say("".join(tline_answer_de ),' ')
        elif language == 'zh-CN':
            self.say(u"当前语言的可用命令如下：")
            self.say(str(tline_answer_zh.encode("utf-8")),' ')
        else:
            self.say("Here are the command which are possible in your language:")
            self.say(tline_answer_en ,' ')
        self.complete_request()