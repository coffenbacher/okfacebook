from django.db import models
import re
from twill.commands import *

# Create your models here.
global LOGGED_IN
LOGGED_IN = False

class Spider(models.Model):
    name = models.CharField(max_length=200)
    #city = models.CharField(max_length=200)
    #other search params

    def crawl_okcupid(self, account):
        pass
    
    def parse_okcupid_html(self, html):
        from okcupid.models import OkCupidProfile
        okids = re.findall('(\w+)\?cf\=', html)
        results = [OkCupidProfile.objects.get_or_create(okid = okid, spider=self) for okid in okids]
    
    def parse_fb_html(self, html):
        from facebook.models import FacebookProfile
        fbids = re.findall('facebook\.com\/([\w\.]+)\?', html)
        for fbid in fbids:
            print FacebookProfile.objects.get_or_create(fbid = fbid, spider=self)


class OkCupidAccount(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def login(self):
        global LOGGED_IN
        if not LOGGED_IN:
            print "Logging in"
            go('https://www.okcupid.com/')
            fv(4, "username", self.username)
            fv(4, "password", self.password)
            submit()
            if not 'nav_matches' in show():
                import ipdb; ipdb.set_trace()
                raise Exception('Failed to log in to OKCupid')
            LOGGED_IN = True
