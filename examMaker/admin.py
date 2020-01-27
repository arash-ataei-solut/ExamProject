from django.contrib import admin
from .models import Question, ExamLevel, Exam


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'question_level')
    list_filter = ('category', 'question_level')


class ExamLevelAdmin(admin.ModelAdmin):
    list_display = ('level_name', )
    list_filter = ('level_name', )


class ExamAdmin(admin.ModelAdmin):
    list_display = ('category', 'level')
    list_filter = ('category', 'level')


admin.site.register(Question, QuestionAdmin)
admin.site.register(ExamLevel, ExamLevelAdmin)
admin.site.register(Exam, ExamAdmin)
