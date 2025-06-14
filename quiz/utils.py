from .models import Badge, UserBadge, QuizAttempt

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