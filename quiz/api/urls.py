#  I created this file 13/06/2025

from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.api_quiz_list, name='api_quiz_list'),  # Returns all quizzes as JSON
    path('attempts', views.api_user_attempts, name='api_user_attempts'),  # Retursn only logged-in user's quiz attempts
    # path('quizzes/', QuizListAPI.as_view(), name='api-quizzes'),
    # path('attempts/<int:user_id>/', UserQuizAttemptAPI.as_view(), name='api-user-attempts'),
    path('quizzes/<int:quiz_id>/', views.api_quiz_detail, name='api_quiz_detail'),
    path('quizzes/<int:quiz_id>/submit/', views.api_submit_quiz, name='api_quiz_detail'),
    path('fetch-quiz/', views.fetch_quiz_from_external_api, name='fetch_quiz_from_external_api'),
    path('fetch-multiple', views.fetch_multiple_categories, name='fetch_multiple_categories'),
]

