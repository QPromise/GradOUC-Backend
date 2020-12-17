from django.contrib import admin
from .models import Config, News, Swiper, Student


# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['begin_day', 'end_day', 'xn', 'xq']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['index', 'news', 'date']


class SwiperAdmin(admin.ModelAdmin):
    list_display = ['url', 'image']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'name', 'passwd', 'department', 'profession',
                    'research', 'supervisor', 'update_date', 'login_date', 'status', 'lock_date']
    search_fields = ['name', 'department', 'supervisor']
    # list_filter = ['department']
    list_per_page = 15


admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Student, StudentAdmin)