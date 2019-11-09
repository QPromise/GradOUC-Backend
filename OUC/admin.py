from django.contrib import admin
from .models import Config,News
# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['begin_day','end_day','xn','xq']
class NewsAdmin(admin.ModelAdmin):
    list_display = ['index','news','date']
admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)

