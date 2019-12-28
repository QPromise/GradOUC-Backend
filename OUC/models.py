from django.db import models
import datetime
# Create your models here.

class Config(models.Model):
    begin_day = models.CharField(max_length=50)
    end_day = models.CharField(max_length=50)
    xn = models.CharField(max_length=50)
    xq = models.CharField(max_length=50)
    # special = models.CharField(max_length=50)

    def __str__(self):
        return self.begin_day
class News(models.Model):
    index = models.IntegerField(default=1)
    news = models.CharField(max_length=200)
    date = models.DateTimeField()
    def __str__(self):
        return self.news
    class Meta():
        ordering=('-date',)
class Swiper(models.Model):
    url = models.CharField(max_length=500)
    image = models.ImageField(upload_to=str('./OUC/static/upload_image/'))
    def get_img_url(self):
        s=str(self.image.url)
        return s[4:]
