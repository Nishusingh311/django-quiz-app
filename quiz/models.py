from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):   #models.Model base class for all models
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit = models.PositiveIntegerField(default=600)  # time limit in seconds default 60s, customizable for each quiz in admin panel

    tags = models.ManyToManyField('Tag', related_name='quizzes', blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes" # for Spelling Mistake (Quizs) in admin panel

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)  # Link to the user who attempted quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)   # # Link to the specific quiz
    score = models.IntegerField()   #store score
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    date_attempted = models.DateTimeField(auto_now_add=True)
    badge = models.CharField(max_length=100, blank=True, null=True)

    def __str__ (self):
        return f"{self.user.username} - {self.quiz.title} ({self.score} %)" # fstring (formatted string literal)
    
class Badge(models.Model): #Details of badge
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_score = models.IntegerField()  #min score to earn this badge

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):      #details of which user earned which Badge
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):    #while prinitinf a Tag object it returns the name
        return self.name   
    