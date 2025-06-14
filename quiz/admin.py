from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, Badge, UserBadge, Tag

#Inline form managing answers nside the question admin
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

# Show answers while editing questions
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz')
    search_fields = ['text']

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'tag_list')
    search_fields = ['title']

    def tag_list(self, obj):
        return ",".join(tag.name for tag in obj.tags.all())
    
#Allows to manage quizzes, questions etc from admin panel
admin.site.register(Quiz, QuizAdmin) #inside ()-> (Quiz  Details, QuizAdmin a custom class to define how it will be displayed)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt) #inside ()-> (Quiz Attempts will be shown , no custom class so django will use the default behaviour to display data)
admin.site.register(Badge) # This allows admin to add badge types
admin.site.register(UserBadge) # This allows admin to who has which badge
admin.site.register(Tag)  #Tags for filtering quiz categories