#  I created this file 13/06/2025
from .serializers import QuizSerializer, QuizAttemptSerializer, QuizDetailSerializer
from quiz.models import Quiz, QuizAttempt, Question, Answer, Tag
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
import requests



# API: get all the quizzes ( List all quizes)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_quiz_list(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

# API: Get attempt history (user must be logged in)
@api_view(['GET'])   #api view (only allows get requests)
@permission_classes([IsAuthenticated])
def api_user_attempts(request):
    attempts = QuizAttempt.objects.filter(user=request.user)
    serializer= QuizAttemptSerializer(attempts, many=True)
    return Response(serializer.data)   #returns the serialized data as a JSON HTTP response

# Quiz details with questions + answers
@api_view(['GET'])
def api_quiz_detail(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({'error':'Quiz not fornd'}, status=404)
    serializer = QuizDetailSerializer(quiz)
    return Response(serializer.data)

# Submit quiz answers via API
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def api_submit_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({'error':'Quiz does not found'}, status=404)
    data = request.data      #  Format: {"answers": {"questions_id: answer_id}}
    questions = Question.objects.filter(quiz=quiz)

    total_questions = questions.count()
    correct = 0
    
    for question in questions:
        selected_id = str(data.get("answers",{}).get(str(question.id)))
        if selected_id:
            try:
                answer = Answer.objects.get(id=selected_id, question=question)
                if answer.is_correct:
                    correct += 1
            except Answer.DoesNotExist:
                continue
    
    score = int((correct/total_questions)*100)

    QuizAttempt.objects.create(
        user = request.user,
        quiz=quiz,
        score=score,
        correct_answers=correct,
        total_questions=total_questions
    )

    return Response({'message':'Quiz submitted successfully', 'score': score})

#  API to list all quiz attempts
# class QuizListAPI(generics.ListAPIView): #ListAPIView Let us show list of data
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer

# # API to list  all attempts by a specific user
# class UserQuizAttemptAPI( generics.ListAPIView):
#     serializer_class = QuizAttemptSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['user_id'] #get user id from url
#         return QuizAttempt.objects.filter(user_id=user_id)




# =====================================================================================
# *********************Fetching Data From External API ********************************
# =====================================================================================

@api_view(['POST']) # This endpoint is for triggeringa data fetch, not retriving
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def fetch_quiz_from_external_api(request):
    # 1. External API endpoint and my API key
    url  = 'https://quizapi.io/api/v1/questions'    # API Endpoint from quizapi.io
    headers = {
        'X-API-Key': 'TJVBF6dlFfLfVWT6Lgkv4BV1RTcpK1eR7FJpGh5r'
    }

    params = {
        'category': 'code',  # can change to 'linux', 'sql', etc.
        'limit': 10,        # Limit he number of questions
    }

    # 2. Make request to external API
    response = requests.get(url, headers=headers, params=params)  #sends a get request to quizapi.io
    data = response.json()               # json parses response into puthon list of dictionaries

    # 3. quiz Object
    quiz = Quiz.objects.create(
        title = "Imported from QuizAPI.io",
        description = "A tech quiz fetched from quizapi.io"
    )

    # Assigning a tag 'QuizAPI' to all the impotred quizzes so admin can identify the imported quizzes
    tag, created = Tag.objects.get_or_create(name="QuizAPI")
    quiz.tags.add(tag)

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

    return Response({'status': 'Quiz imported successfully!'})    # DRF's way of returning data as JSON