from django.contrib import admin
from .models import Config, News, Swiper, Student, SubscribeStudent, StudentRank, StudentInfo
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
                    'score_rank_travel_nj_max']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['index', 'news', 'date']


class SwiperAdmin(admin.ModelAdmin):
    list_display = ['url', 'image']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'sno', 'name', 'passwd', 'department', 'profession',
                    'research', 'supervisor', 'update_date', 'login_date', 'status', 'lock_date']
    search_fields = ['name', 'department', 'profession', 'supervisor', 'sno']
    # list_filter = ['department']
    list_per_page = 15


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
    list_per_page = 15


class StudentInfoAdmin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ['id', 'sno', 'name', 'sex', 'tel', 'date_of_birth', 'id_card', 'home_detail',
                    'department', 'profession', 'research', 'file_unit', 'nation', 'id_info', 'hometown',
                    'start_year', 'study_period', 'degree_type', 'train_type', 'hukou_address',
                    'come_from', 'img_url']
    search_fields = ['sno', 'name', 'department', 'profession', 'research', 'file_unit', 'home_detail']
    list_filter = ['department']
    list_per_page = 15
    actions = ['export_as_excel']


admin.site.register(Config, ConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(SubscribeStudent, SubscribeStudentAdmin)
admin.site.register(StudentRank, StudentRankAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
