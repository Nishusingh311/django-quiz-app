from django.urls import path
from . import views
from .views import signup_view, login_view, logout_view, profile_view
from .api_views import CustomAuthToken

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('api/token-login/', CustomAuthToken.as_view(), name='api_token_login'),
]