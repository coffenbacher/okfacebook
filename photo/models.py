import pickle
from django.db import models
import urllib, cStringIO, urllib2
from PIL import Image
import base64
import imagehash
from facebook.models import FacebookProfile
from okcupid.models import OkCupidProfile

# Create your models here.
class Photo(models.Model):
    url = models.TextField()
    facebook = models.ForeignKey(FacebookProfile, null=True, blank=True, related_name='photos')
    okcupid = models.ForeignKey(OkCupidProfile, null=True, blank=True, related_name='photos')

    _ahash = models.TextField(db_column='ahash')
    _phash = models.TextField(db_column='phash')
    _dhash = models.TextField(db_column='dhash')


    def set_ahash(self, data):
        self._ahash = pickle.dumps(data)

    def get_ahash(self):
        return pickle.loads(self._ahash)

    def set_dhash(self, data):
        self._dhash = pickle.dumps(data)

    def get_dhash(self):
        return pickle.loads(self._dhash)

    def set_phash(self, data):
        self._phash = pickle.dumps(data)

    def get_phash(self):
        return pickle.loads(self._phash)

    ahash = property(get_ahash, set_ahash)
    phash = property(get_phash, set_phash)
    dhash = property(get_dhash, set_dhash)
    
    @classmethod
    def create_from_image(cls, img, url, facebook=None, okcupid=None):
        cls.objects.create(
                ahash = imagehash.average_hash(img),
                phash = imagehash.phash(img),
                dhash = imagehash.dhash(img),
                url = url,
                facebook = facebook,
                okcupid = okcupid)

    @classmethod
    def create_from_url(cls, url, facebook=None, okcupid=None):
        file = cStringIO.StringIO(urllib2.urlopen(url).read())
        img = Image.open(file)
        cls.create_from_image(img, url, facebook=facebook, okcupid=okcupid)



class PhotoMatch(models.Model):
    photos = models.ManyToManyField('Photo')
    a_dist = models.FloatField()
    p_dist = models.FloatField()
    d_dist = models.FloatField()

    @classmethod
    def find_matches(cls, p = 10):
        for okphoto in Photo.objects.filter(okcupid__isnull=False):
            for fbphoto in Photo.objects.filter(facebook__isnull=False):
                if okphoto.dhash - fbphoto.dhash < p and okphoto.pk != fbphoto.pk:
                    o = cls.objects.get_or_create(
                            a_dist = okphoto.ahash - fbphoto.ahash,
                            p_dist = okphoto.phash - fbphoto.phash,
                            d_dist = okphoto.dhash - fbphoto.dhash)
                    o[0].photos = (okphoto, fbphoto)
                    o[0].save()
                    print o
                    
    def __unicode__(self):
        s = "d_dist: %s" % self.d_dist
        for p in self.photos.all():
            if p.facebook:
                s += " http://facebook.com/%s/" % p.facebook.fbid
            if p.okcupid:
                s += " http://okcupid.com/profile/%s/" % p.okcupid.okid

        return unicode(s)
