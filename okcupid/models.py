from django.db import models
import cStringIO
from BeautifulSoup import BeautifulSoup
from spider.models import Spider, OkCupidAccount
import re
import urllib2
from PIL import Image
from twill.commands import *

# Create your models here.

class OkCupidProfile(models.Model):
    okid = models.CharField(max_length=200)
    spider = models.ForeignKey(Spider)
    scraped = models.BooleanField(default=False)

    def scrape(self):
        from photo.models import Photo
        o = OkCupidAccount.objects.all()[0]
        o.login()
        agent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')

        url = 'http://www.okcupid.com/profile/%s/photos?cf=regular_indirect' % self.okid
        go(url)
        html = show()
        b = BeautifulSoup(html)
        divs = b.findAll('div', {'class': 'pic clearfix'})
        for div in divs:
            img_tag = div.find('img')
            try:
                Photo.create_from_url(url=img_tag['src'], okcupid=self)
            except:
                print "no img found"

        self.scraped = True
        self.save()

    @classmethod
    def scrape_all(cls):
        for p in cls.objects.filter(scraped=False):
            p.scrape()
