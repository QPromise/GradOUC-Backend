from django.db import models
import datetime
# Create your models here.


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
    is_open_rank_score_update = models.IntegerField('是否允许学生更新成绩排名的成绩(0:不开启,1:开启,2:只开启管理员的)', default=1)

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
    class_duties = models.SmallIntegerField('职务(0学生 1班长 2支书 3 学习委员  10其它)', default=0)
    extra = models.TextField('其它信息', default="-")
    update_date = models.DateTimeField('最新登录日期', auto_now=True)
    login_date = models.DateTimeField('注册日期', auto_now_add=True)
    status = models.IntegerField('用户状态(0:正常,1:问题,2:禁用)', default=0)
    lock_date = models.DateTimeField('禁用日期', null=True, blank=True)

    class Meta(object):
        ordering = ('-update_date',)


class StudentRank(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField('openid', max_length=50, db_index=True, unique=True)
    sno = models.CharField('学号', max_length=15, default="-", db_index=True)
    avg_score = models.CharField('平均学分绩', max_length=10, default="-")
    avg_score_update_date = models.DateTimeField('学分绩更新日期', auto_now=True)
    department = models.CharField('学院', max_length=20, db_index=True, default="-")
    profession = models.CharField('专业', max_length=40, default="-")
    research = models.CharField('研究方向', max_length=40, default="-")
    can_join_rank = models.IntegerField('是否可以参与排名(0:不及格或重修,1:正常)', default=1)
    rank_research = models.CharField('参与排名的研究方向', max_length=1024, default="-")
    exclude_courses = models.CharField('不参与排名的课程名称及类型', max_length=256, default="-")
    courses_name = models.CharField('课程名称', max_length=1024, default="-")
    courses_type = models.CharField('课程类型', max_length=1024, default="-")
    courses_info = models.TextField('课程信息', default="-")
    travel_nums = models.IntegerField('遍历次数', default=0)

    class Meta(object):
        index_together = ["profession", "research", "can_join_rank"]


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

    class Meta(object):
        indexes = [models.Index(fields=['status'], name="idx_status")]


class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    sno = models.CharField('学号', max_length=15, default="-", db_index=True, unique=True)
    name = models.CharField('姓名', max_length=15, default="-", db_index=True)
    sex = models.CharField('性别', max_length=5, default="-")
    date_of_birth = models.CharField('出生日期', max_length=15, default="-")
    id_card = models.CharField('身份证号', max_length=20, default="-")
    nation = models.CharField('民族', max_length=20, default="-")
    id_info = models.CharField('个人信息', max_length=20, default="-")
    hometown = models.CharField('籍贯', max_length=100, default="-")
    start_year = models.CharField('年级', max_length=4, default="-")
    study_period = models.CharField('学制', max_length=10, default="-")
    degree_type = models.CharField('学位类别', max_length=10, default="-")
    train_type = models.CharField('培养类型', max_length=10, default="-")
    hukou_address = models.CharField('户口所在地', max_length=100, default="-")
    home_tel = models.CharField('家庭电话', max_length=20, default="-")
    home_postcode = models.CharField('家庭邮编', max_length=10, default="-")
    home_detail = models.CharField('家庭地址', max_length=100, default="-")
    come_from = models.CharField('来源', max_length=50, default="-")
    file_unit = models.CharField('档案所在单位', max_length=50, default="-")
    tel = models.CharField('电话', max_length=20, default="-")
    department = models.CharField('学院', max_length=20, db_index=True, default="-")
    profession = models.CharField('专业', max_length=40, db_index=True, default="-")
    research = models.CharField('研究方向', max_length=40, db_index=True, default="-")
    img_url = models.CharField('个人照片', max_length=65, default="-")


class IPProxy(models.Model):
    proxy_ip = models.CharField('代理ip', max_length=50, default="-")
    get_ip_time = models.CharField('获取时间', max_length=20, default="-")
    update_date = models.DateTimeField('最新获取日期', auto_now=True)
    rest_time = models.IntegerField('剩余时间', max_length=10, default=298)
    force_update = models.IntegerField('是否强制更新(1为强制，0为没有)', default=0)


class DreamOUCProfession(models.Model):
    department_name = models.CharField('学院名称', max_length=30, default="信息科学与工程学院")
    profession_name = models.CharField('专业名称', max_length=30, default="-")
    profession_hot_val = models.IntegerField('专业热度', max_length=10, default=390)
    profession_material_title = models.CharField('资料及经验名称(10个字左右)', max_length=20, default="资料内容介绍及备考经验")
    profession_material_url = models.CharField('资料及经验地址(微信文章跳转)', max_length=100, default="-")
    open_course_title = models.CharField('公开课名称', max_length=20, default="免费高分学长/学姐经验分享公开课")
    open_course_url = models.CharField('公开课地址', max_length=100, default="-")
    taobao_key = models.CharField('淘口令', max_length=100, default="-")
    update_intro = models.CharField('上新说明(不超过4个字)', max_length=10, default="-")
    profession_material_description = models.TextField('其它说明', default="-")


class DreamOUCNews(models.Model):
    id = models.AutoField(primary_key=True)
    news_title = models.CharField('标题', max_length=50, default="-")
    news_url = models.CharField('内容地址', max_length=100, default="-")
    news_tag = models.CharField('标签(#分割开，总共不超过12个字)', max_length=30, default="-")
    news_is_top = models.SmallIntegerField('是否置顶（1为置顶，0为没有）', default=0)
    news_top_val = models.SmallIntegerField('置顶优先级，数字越大越靠前', default=0)
    published_time = models.DateTimeField('发布时间')
    modified_time = models.DateTimeField('修改时间', auto_now=False)
    news_attention = models.IntegerField('查看次数', max_length=10, default=10)
    news_hot_val = models.IntegerField('热度值', max_length=10, default=0)

    class Meta(object):
        ordering = ('-published_time',)
