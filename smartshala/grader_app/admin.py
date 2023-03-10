from django.contrib import admin

from .models import AnsweredQuestion, AnswerSheet, StudentGrade

# Register your models here.

admin.site.register(AnsweredQuestion)
admin.site.register(StudentGrade)
admin.site.register(AnswerSheet)
