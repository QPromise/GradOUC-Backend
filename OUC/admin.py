from django.contrib import admin
from .models import Config, News, Swiper, Student, SubscribeStudent, StudentRank


# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['begin_day', 'end_day', 'xn', 'xq', 'is_open_subscribe',
                    'is_open_score_rank_travel', 'get_score_rank_nj_max',
                    'get_score_rank_nj_min', 'score_rank_travel_nj_min',
                    'score_rank_travel_nj_max']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['index', 'news', 'date']


class SwiperAdmin(admin.ModelAdmin):
    list_display = ['url', 'image']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'name', 'passwd', 'department', 'profession',
                    'research', 'supervisor', 'update_date', 'login_date', 'status', 'lock_date']
    search_fields = ['name', 'department', 'supervisor', 'sno']
    # list_filter = ['department']
    list_per_page = 15


class SubscribeStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'scores', 'status', 'failure_popup', 'travel_nums',
                    'send_success_nums', 'send_fail_nums', 'new_send_message', 'legal_subscribe_date', 'subscribe_date']
    search_fields = ['sno']
    list_per_page = 15


class StudentRankAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'avg_score', 'avg_score_update_date', 'department',
                    'profession', 'research', 'rank_research', 'travel_nums']
    search_fields = ['sno']
    list_per_page = 15


admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(SubscribeStudent, SubscribeStudentAdmin)
admin.site.register(StudentRank, StudentRankAdmin)
