from django.contrib import admin
from .models import Config, News, Swiper, Student, SubscribeStudent, StudentRank, StudentInfo, IPProxy, \
    DreamOUCProfession, DreamOUCNews
from openpyxl import Workbook
from django.http import HttpResponse


class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for obj in queryset:
            for field in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]
            row = ws.append(data)

        wb.save(response)
        return response

    export_as_excel.short_description = '导出Excel'


# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['begin_day', 'end_day', 'xn', 'xq', 'is_open_subscribe',
                    'is_open_score_rank_travel', 'get_score_rank_nj_max',
                    'get_score_rank_nj_min', 'score_rank_travel_nj_min',
                    'score_rank_travel_nj_max', 'is_open_rank_score_update']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['index', 'news', 'date']


class SwiperAdmin(admin.ModelAdmin):
    list_display = ['url', 'image']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'name', 'passwd', 'department', 'profession',
                    'research', 'supervisor', 'class_duties', 'extra', 'update_date', 'login_date', 'status', 'lock_date']
    search_fields = ['name', 'department', 'profession', 'supervisor', 'sno']
    # list_filter = ['department']
    list_per_page = 20


class SubscribeStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'scores', 'status', 'failure_popup', 'travel_nums',
                    'send_success_nums', 'send_fail_nums', 'new_send_message', 'legal_subscribe_date', 'subscribe_date']
    search_fields = ['sno']
    list_per_page = 15


class StudentRankAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'avg_score', 'can_join_rank', 'avg_score_update_date', 'department',
                    'profession', 'research', 'rank_research', 'exclude_courses', 'courses_name', 'courses_type',
                    'courses_info', 'travel_nums']
    search_fields = ['sno']
    list_per_page = 20


class StudentInfoAdmin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ['id', 'sno', 'name', 'sex', 'tel', 'date_of_birth', 'id_card', 'home_detail',
                    'department', 'profession', 'research', 'file_unit', 'nation', 'id_info', 'hometown',
                    'start_year', 'study_period', 'degree_type', 'train_type', 'hukou_address',
                    'come_from', 'img_url']
    search_fields = ['sno', 'name', 'department', 'profession', 'research', 'file_unit', 'home_detail']
    list_filter = ['department']
    list_per_page = 20
    actions = ['export_as_excel']


class IPProxyAdmin(admin.ModelAdmin):
    list_display = ['proxy_ip', 'get_ip_time', 'update_date', 'rest_time', 'force_update']


class DreamOUCProfessionAdmin(admin.ModelAdmin):
    list_display = ['department_name', 'profession_name', 'profession_hot_val', 'profession_material_title',
                    'profession_material_url', 'open_course_title', 'open_course_url', 'taobao_key',
                    'update_intro', 'profession_material_description']
    list_filter = ['department_name']


class DreamOUCNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'news_title', 'news_url', 'news_tag', 'news_is_top', 'news_top_val',
                    'published_time', 'modified_time', 'news_attention', 'news_hot_val']


admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(SubscribeStudent, SubscribeStudentAdmin)
admin.site.register(StudentRank, StudentRankAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(IPProxy, IPProxyAdmin)
admin.site.register(DreamOUCProfession, DreamOUCProfessionAdmin)
admin.site.register(DreamOUCNews, DreamOUCNewsAdmin)
