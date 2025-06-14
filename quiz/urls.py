from django.urls import path, include
from . import views
from .views import leaderboard_view

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/',views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('<int:quiz_id>/export/', views.export_results_csv, name='export_results'),
    path('quiz/<int:quiz_id>/export/pdf/', views.export_results_pdf, name='export_results_pdf'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/', include('quiz.api.urls')),
    path('api/', include('quiz.api.urls')),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('quiz/<int:quiz_id>/question/<int:question_view>', views.question_view, name='question_view'),  # example: quiz/5/question/1
    path('quiz/<int:quiz_id>/result/', views.quiz_result_view, name='quiz_result'),
    path('quiz-analytics/', views.admin_quiz_analytics, name='admin_quiz_analytics'),
    path('api/', include('quiz.api.urls')),

    # API endpoints
    # path('api/quizzes/',views.api_quiz_list, name='api_quiz_list'), # Returns all quizzes as JSON
    # path('api/my_attempts/', views.api_user_attempts, name='api_user_attempts'), # Retursn only logged-in user's quiz attempts
]