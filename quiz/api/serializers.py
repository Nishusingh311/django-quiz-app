#  I created this file 13/06/2025
#A serializer converts complex data like django model instances(objects) into Python datattypes(like dictionaries) that can be easily rendered into json - and also the reverse ( for saving data into the database)
# In Django rest framework serializers work as a form - it validates input and also converts Python Data (like model objects) into JSON (which APIs use).
from rest_framework import serializers
from quiz.models import Quiz, Question, Answer, QuizAttempt


# Serializer for the Answer model : used inside questions to show possible options
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct'] #Field to include in JSON


# Serializer for the Question model : (serializes questions with all answers) used inside quiz to show full question-answer structure
class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True ) #Include Related answers
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'answer_set']


# Serializer for the Quiz model : (serializes quizzes with questions and answers) full quiz export for users
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']


# Serializer for quiz details : (another version to export full quiz detail), same purpose as QuizSerializer, different field layout
class QuizDetailSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True,read_only=True)

    class Meta:
        model = Quiz
        fields=['id', 'title','description','question_set']


# Serializer for the Attempts model : (serializes each user's attempt on quiz)  Useful for history or analytics
class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz= serializers.StringRelatedField()     # Show quiz title
    class Meta:
        model = QuizAttempt
        fields = ['quiz', 'score', 'correct_answers', 'total_questions', 'date_attempted']