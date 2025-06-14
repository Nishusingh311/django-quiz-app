from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from quiz.models import UserBadge, QuizAttempt
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])   # Hash Password
            user.save()
            Token.objects.create(user=user)  # Creates a unique token for users, can be used to access protected api endpoints
            messages.success(request, 'Account created successfully')

            # Email notification
            send_mail(
                subject= 'Welcome to QuizApp!',
                message = 'Thanks for signing up! Start attempting quizzes and earn badges!',
                from_email=None,
                recipient_list=[user.email],
                fail_silently= True,
            )
            
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html',{'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or Password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
    
# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    #fetching All attempts by logged-in user
    attempts = QuizAttempt.objects.filter(user=request.user)

    total_attempts = attempts.count()

    if total_attempts > 0:
        average_score = sum(attempt.score for attempt in attempts)/ total_attempts
    else:
        average_score = 0

    # fetching badges earned by user
    badges = UserBadge.objects.filter(user=request.user)

    return render(request, 'accounts/profile.html',
     {
         'attempts': attempts,
         'total_attempts': total_attempts,
         'average_score' : round(average_score,2),
         'badges': badges
     })
