from django.db import models
from spider.models import Spider
import urllib2
import cStringIO
from PIL import Image

# Create your models here.

class FacebookProfile(models.Model):
    fbid = models.CharField(max_length=200)
    spider = models.ForeignKey(Spider)
    scraped = models.BooleanField(default=False)

    def __unicode__(self):
        return self.fbid

    def scrape(self):
        from photo.models import Photo
        img_url = 'https://graph.facebook.com/%s/picture' % self.fbid
        try:
            Photo.create_from_url(img_url, facebook=self)
            self.scraped = True
            self.save()
        except:
            print "some issue with %s" % img_url

    @classmethod
    def scrape_all(cls):
        for f in cls.objects.filter(scraped=False):
            f.scrape()
