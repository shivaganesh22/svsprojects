from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video)
admin.site.register(Questions)
admin.site.register(Quizs)
admin.site.register(StudentResponse)
admin.site.register(ExamResult)