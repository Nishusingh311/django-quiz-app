from django.contrib import admin, messages
from .models import Quiz, Question, Answer, QuizAttempt, Badge, UserBadge, Tag
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import redirect
import requests 
from .utils import fetch_quiz_from_quizapi

#Inline form managing answers nside the question admin
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

# Show answers while editing questions
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz')
    search_fields = ['text']


# # For Adding Panel Button to Trigger Quiz Fetching from API
@admin.action(description="Import quizzes from QuizAPI.io")
def import_from_quizapi(modeladmin, request, queryset):
    API_KEY = 'TJVBF6dlFfLfVWT6Lgkv4BV1RTcpK1eR7FJpGh5r'
    categories = ['code', 'linux', 'bash', 'docker', 'cms', 'sql', 'devops']  #choose which categories to import
    fetch_quiz_from_quizapi(categories, API_KEY) #calling function from utils.py
    messages.success(request, "QuizAPI quizzes imported successfully")


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'tag_list')
    search_fields = ['title']
    actions = [import_from_quizapi]
    
    def tag_list(self, obj):
        return ",".join(tag.name for tag in obj.tags.all())   #shows a comma separeted list of tags for each quiz ex: python, c++ 
    
    def import_quiz_from_api(self, request, queryset):
        return redirect('admin:fetch_quiz_from_api')
    
    import_quiz_from_api.short_description = "Import Quiz from QuizAPI.io (No Selection Needed)"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fetch-quiz-api/', self.admin_site.admin_view(self.fetch_quiz_from_api_view), name='fetch_quiz_from_api')
        ]
        return custom_urls + urls
    
    def fetch_quiz_from_api_view(self, request):
        url = 'https://quizapi.io/api/v1/questions'
        headers = {
            'X-API-Key': 'TJVBF6dlFfLfVWT6Lgkv4BV1RTcpK1eR7FJpGh5r'
        }

        category = ['code', 'linux', 'bash', 'docker', 'cms', 'sql', 'devops'],  #choose which categories to import,

 
        params = {
            'category': category,
            'limit': 5
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        quiz = Quiz.objects.create(
            title = "Quiz from QuizAPI.io",
            description = "A quiz fetched from QuizAPI.io"
        )

        quiz.tags.add(Tag.objects.get_or_create(name="QuizAPI")[0])
        quiz.tags.add(Tag.objects.get_or_create(name=category.capitalize())[0])

        
        # 4. Loop through the questions and save to DB
        for item in data:
            question = Question.objects.create(
            quiz=quiz,
            text=item['question']
            )

            # Answers from API are dictionary like {'ans1':"..", 'ans2':"..."}
            for key, value in item['answers'].items():
                if value:
                    is_correct = key == item.get('correct_answer')    # is_correct = key: checks if the current key(like 'answer_a') matches the correct answer, item.get('correct_answer') gets the answer (like 'answer_b) so is_correct='answer_a' == 'answer_b' will be False
                    # Only one answer will get is_correct = True all others get False
                    Answer.objects.create(
                        question=question,
                        text=value,
                        is_correct=is_correct
                    )
        self.message_user(request,"QuizAPI quizzes imported successfully", level=messages.SUCCESS )
        return HttpResponseRedirect(reverse('admin:quiz_quiz_changelist'))

#Allows to manage quizzes, questions etc from admin panel
admin.site.register(Quiz, QuizAdmin) #inside ()-> (Quiz  Details, QuizAdmin a custom class to define how it will be displayed)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt) #inside ()-> (Quiz Attempts will be shown , no custom class so django will use the default behaviour to display data)
admin.site.register(Badge) # This allows admin to add badge types
admin.site.register(UserBadge) # This allows admin to who has which badge
admin.site.register(Tag)  #Tags for filtering quiz categories
admin.site.register(Answer) 