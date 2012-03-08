import threading, urllib2

class AsyncOpenHttp(threading.Thread):
    def __init__(self, successCallback, errorCallback):
        super(AsyncOpenHttp, self).__init__()
        self.successCallback = successCallback
        self.errorCallback = errorCallback
        self.finished = True
    
    def make_google_request(self, flac, requestId, dictation, language="en-US", allowCurses=True):
        if self.finished:
            self.currentFlac = flac
            self.requestId = requestId
            self.dictation = dictation
            self.language = language
            self.allowCurses = allowCurses
            self.finished = False
            self.run()
    
    def run(self):
        # of course change urllib to httplib-something-something
        url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter={0}&lang={1}&maxresults=6".format(0 if self.allowCurses else 2, self.language)
        req = urllib2.Request(url, data = self.currentFlac, headers = {'Content-Type': 'audio/x-flac; rate=16000', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21'})
        try:
            content  = urllib2.urlopen(req, timeout=10).read()
            self.finished = True
            self.successCallback(content, self.requestId, self.dictation)
        except:
            self.finished = True
            self.errorCallback(self.requestId, self.dictation)
