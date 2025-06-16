from .models import Badge, UserBadge, QuizAttempt, Quiz, Question, Answer, Tag
import requests

def assign_badges(user, score, quiz_attempt=None):
    badges = Badge.objects.all()
    for badge in badges:
        already_awarded = UserBadge.objects.filter(user=user, badge=badge).exists()
        if already_awarded:
            continue

        if badge.name == 'Perfect Score' and score == 100:
            UserBadge.objects.create(user=user, badge=badge)
            if quiz_attempt:
                quiz_attempt.badge = badge.name
                quiz_attempt.save()

        elif badge.name == 'High Scorer' and score >= 90:
            UserBadge.objects.create(user=user, badge=badge)
            if quiz_attempt:
                quiz_attempt.badge = badge.name
                quiz_attempt.save()

        elif badge.name == 'Quiz Explorer':
            total_attempts = QuizAttempt.objects.filter(user=user).count()
            if total_attempts >= 3:
                UserBadge.objects.create(user=user, badge=badge)
                if quiz_attempt:
                    quiz_attempt.badge = badge.name
                    quiz_attempt.save()


# For Adding Panel Button to Trigger Quiz Fetching from API
def fetch_quiz_from_quizapi(categories, api_key):
    url = 'https://quizapi.io/api/v1/questions'
    headers = {
        'X-API-Key': api_key
    }

    for category in categories:
        params = {
            'category': category,
            'limit': 5
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        quiz = Quiz.objects.create(
            title = f"{category.capitalize()} Quiz from QuizAPI.io",
            description = f"A {category} quiz fetched from QuizAPI.io"
        )

        quiz.tags.add(Tag.objects.get_or_create(name="WuizAPI")[0])
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


# from quiz.models import Badge, QuizAttempt, UserBadge

# def assign_badges(user, score):
#     badges = Badge.objects.all()
#     latest_attempt = QuizAttempt.objects.filter(user=user).latest('date_attempted')

#     for badge in badges:
#         already_awarded = UserBadge.objects.filter(user=user, badge=badge).exists()
#         if not already_awarded:
#             if badge.name == 'Perfect Score' and score == 100:
#                 UserBadge.objects.create(user=user, badge=badge)
#                 latest_attempt.badge = badge.name
#                 latest_attempt.save()

#             elif badge.name == 'High Scorer' and score >= 90:
#                 UserBadge.objects.create(user=user, badge=badge)
#                 latest_attempt.badge = badge.name
#                 latest_attempt.save()

#             elif badge.name == 'Quiz Explorer':
#                 total_attempts = QuizAttempt.objects.filter(user=user).count()
#                 if total_attempts >= 3:
#                     UserBadge.objects.create(user=user, badge=badge)
#                     latest_attempt.badge = badge.name
#                     latest_attempt.save()

# def assign_badges(user, score, quiz_attempt=None):
#     badges = Badge.objects.all()
#     for badge in badges:
#         already_awarded = UserBadge.objects.filter(user=user, badge=badge).exists()
#         if not already_awarded:
#             if badge.name == 'Perfect Score' and score == 100:
#                 UserBadge.objects.create(user=user, badge=badge)
#                 if quiz_attempt:
#                     quiz_attempt.badge = badge.name
#                     quiz_attempt.save()
#             elif badge.name == 'High Scorer' and score >= 90:
#                 UserBadge.objects.create(user=user, badge=badge)
#                 if quiz_attempt:
#                     quiz_attempt.badge = badge.name
#                     quiz_attempt.save()
#             elif badge.name == 'Quiz Explorer':
#                 total_attempts = QuizAttempt.objects.filter(user=user).count()
#                 if total_attempts >= 3:
#                     UserBadge.objects.create(user=user, badge=badge)
#                     if quiz_attempt:
#                         quiz_attempt.badge = badge.name
#                         quiz_attempt.save()