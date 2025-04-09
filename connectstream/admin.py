from django.contrib import admin

# Register your models here.
from .models import Question, Answer
class Question_admin(admin.ModelAdmin):
    list_display= ('title', 'description','created_by' )

admin.site.register(Question, Question_admin)

class Answer_admin(admin.ModelAdmin):
    list_display= ('answered_by', 'question','created_at' )

admin.site.register(Answer, Answer_admin)
