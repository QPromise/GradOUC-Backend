from django.db import models
import datetime
# Create your models here.


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField('openid', max_length=50, db_index=True)
    sno = models.CharField('学号', max_length=15, default="-", db_index=True)
    name = models.CharField('姓名', max_length=20, default="-")
    passwd = models.CharField('密码', max_length=20, default="-")
    department = models.CharField('学院', max_length=20, default="-")
    profession = models.CharField('专业', max_length=40, default="-")
    research = models.CharField('研究方向', max_length=40, default="-")
    supervisor = models.CharField('导师', max_length=20, default="-")
    update_date = models.DateTimeField('最新登录日期', auto_now=True)
    login_date = models.DateTimeField('注册日期', auto_now_add=True)
    status = models.IntegerField('用户状态(0:正常,1:问题,2:禁用)', default=0)
    lock_date = models.DateTimeField('禁用日期', null=True, blank=True)

    class Meta(object):
        ordering = ('-update_date',)


class Config(models.Model):
    begin_day = models.CharField('开始日期(如2020-08-24 00:00:00)', max_length=50)
    end_day = models.CharField('结束日期(如2021-01-26 00:00:00)', max_length=50)
    xn = models.CharField('学年(如2020)', max_length=50)
    xq = models.CharField('学期(如2020-2021夏秋)', max_length=50)
    # special = models.CharField(max_length=50)

    def __str__(self):
        return self.begin_day


class News(models.Model):
    index = models.IntegerField(default=1)
    news = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return self.news

    class Meta(object):
        ordering = ('-date',)


class Swiper(models.Model):
    url = models.CharField(max_length=500)
    image = models.ImageField(upload_to=str('./OUC/static/upload_image/'))

    def get_img_url(self):
        s = str(self.image.url)
        return s[4:]
