from django.contrib import admin

from .models import Quiz, Question, Answer, TakenQuiz, Student, StudentAnswer
from .forms import BaseAnswerInlineFormSet, QuestionAdminForm
from app.mixins import ExportCsvMixin



admin.site.register(Answer)
admin.site.register(StudentAnswer)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name','published','time','created','updated']
    raw_id_fields = ['owner']


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 4
    max_num = 4
    min_num = 4
    validate_min=True
    validate_max=True
    formset = BaseAnswerInlineFormSet
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ AnswerInline]
    form = QuestionAdminForm


class ScoreListFilter(admin.SimpleListFilter):
    title = 'score'
    parameter_name = 'score'

    def lookups(self, request, model_admin):
       
        return (
            ('failed', 'Failed'),
            ('passed', 'Passed'),
        )

    def queryset(self, request, queryset):
       
        if self.value() == 'failed':
            return queryset.filter(score__gte=0.0,
                                    score__lte=39.0)
        if self.value() == 'passed':
            return queryset.filter(score__gte=40.0,
                                    score__lte=100.0)


@admin.register(TakenQuiz)
class TakenQuizAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['student','quiz', 'phone', 'email','score', 'date']
    list_filter = ['date', ScoreListFilter]
    search_fields = ['student']
    actions = ["export_as_csv"] 

    ExportCsvMixin.export_as_csv.short_description = 'Export selected records to csv'
    