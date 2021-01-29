from django.db import models
import datetime
# Create your models here.


class StudentRank(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField('openid', max_length=50, db_index=True, unique=True)
    sno = models.CharField('学号', max_length=15, default="-", db_index=True)
    avg_score = models.CharField('平均学分绩', max_length=10, default="-")
    avg_score_update_date = models.DateTimeField('学分绩更新日期', auto_now=True)
    department = models.CharField('学院', max_length=20, db_index=True, default="-")
    profession = models.CharField('专业', max_length=40, db_index=True, default="-")
    research = models.CharField('研究方向', max_length=40, db_index=True, default="-")
    rank_research = models.CharField('参与排名的研究方向', max_length=1024, default="-")
    exclude_courses = models.CharField('不参与排名的科目', max_length=256, default="-")
    courses_name = models.CharField('课程名称', max_length=1024, default="-")
    courses_info = models.TextField('课程信息', default="-")
    travel_nums = models.IntegerField('遍历次数', default=0)

    # def save(self, *args, **kwargs):
    #     self.avg_score = float(self.avg_score)
    #     super(StudentRank, self).save(*args, **kwargs)


class SubscribeStudent(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField('openid', max_length=50, db_index=True, unique=True)
    sno = models.CharField('学号', max_length=15, default="-", db_index=True)
    scores = models.CharField('成绩', max_length=256, default="-")
    status = models.IntegerField('订阅次数(1及其以上为订阅，0为没有)', default=0)
    failure_popup = models.IntegerField('是否失效弹窗(1为失效弹窗，0为失效不弹窗)', default=1)
    travel_nums = models.IntegerField('遍历次数', default=0)
    send_success_nums = models.IntegerField('发送成功次数', default=0)
    send_fail_nums = models.IntegerField('发送失败次数', default=0)
    new_send_message = models.CharField('最新发送的成绩', max_length=256, default="-")
    legal_subscribe_date = models.CharField('每次订阅的时间戳（有效期七天以内）', max_length=1024, default="-")
    subscribe_date = models.DateTimeField('订阅日期', auto_now_add=True)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField('openid', max_length=50, db_index=True, unique=True)
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
    is_open_subscribe = models.IntegerField('是否开启成绩通知(0:未开启,1:开启,2:只开启管理员的)', default=0)
    is_open_score_rank_travel = models.IntegerField('是否开启成绩排名的遍历(0:未开启,1:开启,2:只开启管理员的)', default=0)
    get_score_rank_nj_min = models.CharField('参与成绩排名的年级下限', max_length=5, default="2120")
    get_score_rank_nj_max = models.CharField('参与成绩排名的年级上限', max_length=5, default="2120")
    score_rank_travel_nj_min = models.CharField('成绩排名遍历的年级下限', max_length=5, default="2120")
    score_rank_travel_nj_max = models.CharField('成绩排名遍历的年级上限', max_length=5, default="2120")

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
