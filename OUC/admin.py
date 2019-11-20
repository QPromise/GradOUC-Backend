from django.contrib import admin
from .models import Config,News,Swiper
# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['begin_day','end_day','xn','xq']
class NewsAdmin(admin.ModelAdmin):
    list_display = ['index','news','date']
class SwiperAdmin(admin.ModelAdmin):
    list_display = ['url','image']
admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Swiper, SwiperAdmin)

