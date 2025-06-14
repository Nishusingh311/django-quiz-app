from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Quiz, Question, Answer, QuizAttempt, Badge, UserBadge
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
import json
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Avg, Count
from .utils import assign_badges
from django.core.mail import send_mail
from .models import Quiz, QuizAttempt, Tag
from django.core.paginator import Paginator
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from datetime import timedelta,datetime
from django.utils.timezone import now

# Create your views here.
def home(request):
    query = request.GET.get('q','')   # Get search query from URL
    if query:
        quizzes = Quiz.objects.filter(title__icontains=query) #title_icontains searches titles case-insensitively 
    else:
        quizzes = Quiz.objects.all()

    # Add pagination: Show 10 quizzes oer page
    paginator = Paginator(quizzes, 10)
    page_number = request.GET.get('page')
    page_obj  = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'quizzes': page_obj, # send paginated quizzes to template
        'query': query,
        'request': request    # So we can show the current query i search box
        })

def quiz_list(request):
    tag_id = request.GET.get('tag')    # get tag ID from (URL) query string like ?tag=3

    if tag_id: # if tag filter is applied
        quizzes = Quiz.objects.filter(tags__id=tag_id) # tags__id=tag_id is a manytomany field: this filters quizzes having tag ID
    else: 
        quizzes = Quiz.objects.all() # fetches all quizes from database

    tags = Tag.objects.all()  # Fetch all tags from database to show in filter menu

    return render(request, 'quiz/quiz_list.html',{
        'quizzes': quizzes,   # passes the filtered or full quiz list to the template
        'tags': tags,    # passes all tag options to display
        'selected_tag_id': int(tag_id) if tag_id else None  # helps UI to highlight selected tag
        })


@login_required
def quiz_detail(request, quiz_id): # quiz_id is the dynamic parameter coming from the URL to identify which quiz the user is taking
    quiz = Quiz.objects.get(id=quiz_id)  #get the selected quiz using ID
    
    # Fetch questions in random order using order_by('?'): this will fetch questions in random order
    questions = Question.objects.filter(quiz=quiz).order_by('?').prefetch_related('answer_set') # Load questions & answers for that quiz
    # prefetch_related('answer_set') fetch related asswers for each question efficiently

    if request.method == 'POST':
        total_questions = questions.count()
        correct = 0
        pass

        for question in questions:
            selectd_answer_id = request.POST.get(f'question_{question.id}')
            if selectd_answer_id:
                selectd_answer = Answer.objects.get(id=selectd_answer_id)  # if user selected and answer fetch it from DB
                if selectd_answer.is_correct: 
                    correct += 1
        
        score = int((correct / total_questions)*100)


        # Save the quiz attempt to DB
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            correct_answers=correct,
            total_questions=total_questions,
        )


        # Assign badges based on score and attempt count
        assign_badges(request.user, score, quiz_attempt=attempt)

        # Send mail to the user
        send_mail(
            subject= f'Quiz Result: {quiz.title}',
            message= f'Hi {request.user.username}, \n\nYou scored {score}% on "{quiz.title}". \n Correct Answers" {correct} out of {total_questions}. \n\nGood luck for the next one! ',
            from_email= None,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

        return render (request, 'quiz/quiz_result.html',{'quiz':quiz, 
                                                        'score': score, 
                                                        'correct' : correct,
                                                        'total': total_questions})

    return render(request, 'quiz/quiz_detail.html', {'quiz':quiz, 
                                                     'questions': questions})


@login_required
def dashboard(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-date_attempted')
    return render( request, 'quiz/dashboard.html', {'attempts' : attempts})

@login_required
def profile_view(request):
    user = request.user
    attempts = user.quizattempt_set.all()
    return render( request, 'quiz/profile.html',{
        'user': user,
        'attempts': attempts
    })

@login_required
def export_results_csv(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz)

    #Http response with csv content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}"_results.csv'

    writer =csv.writer(response)
    writer.writerow(['Username', 'Score (%)', 'Correct Answers', 'Total Questions', 'Date Attempted'])

    for attmept in attempts:
        writer.writerow([
            attmept.user.username,
            attmept.score,
            attmept.correct_answers,
            attmept.total_questions,
            attmept.date_attempted.strftime("%Y-%m-%d %H:%M"),
        ])
    
    return response

@login_required
def export_results_pdf(request, quiz_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    
    quiz = Quiz.objects.get(id=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz)
    
    template_path = 'quiz/quiz_results_pdf.html'
    context = {'quiz':quiz, 'attempts': attempts}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispositio'] = f'filename="{quiz.title}_results.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    
    return response

@login_required
def leaderboard(request):
    top_users = (
        QuizAttempt.objects
        .values('user__username')
        .annotate(avg_score=Avg('score'))
        .order_by('-avg_score')[:10]
        )
    
    return render(request, 'quiz/leaderboard.html', {'top_users': top_users})


def leaderboard_view(request):
    # Get query param from URL: ? range= weekly or ?range=monthly
    range_filter = request.GET.get('range', 'weekly')   # default is weekly

    if range_filter == 'monthly':
        time_threshold = now() - timedelta(days=30)
    else:
        time_threshold = now() - timedelta(days=7)

    # Filter attempts within timerange
    attempts = QuizAttempt.objects.filter(date_attempted__gte=time_threshold)   # Fetches quiz attempts done after time_threshold only

    # Annotate average score for each user
    leaderboard = (
        attempts.values('user__username')  # group by username
        .annotate(avg_score=Avg('score'))  #calculate average score
        .order_by('-avg_score')[:10]   #Top 10
    )

    return render(request, 'quiz/leaderboard.html',{
        'leaderboard': leaderboard,
        'range': range_filter,
    })


# Questions View (1 question per page)
@login_required
def question_view(request, quiz_id, question_number):
    quiz= get_object_or_404(Quiz, id=quiz_id)
    questions = list(Question.objects.filter(quiz=quiz).order_by('id'))  #get all questions in this quiz

    # check if quiz has questions
    if question_number> len(questions):
        return redirect('quiz_result', quiz_id=quiz.id)
    
    current_question = questions[question_number - 1]
    answers = current_question.answer_set.all()

    if request.method == 'POST':  # on form submission save answer and move to next question
        selected_answer_id = request.POST.get('answer')
        if not request.session.get('quiz_data'):       #usedjango session to save users answers without saving it to DB yet
            request.session['quiz_data'] = {}

        request.session['quiz_data'][str(current_question.id)] = selected_answer_id
        request.session.modified = True

        # Move to next Question
        return redirect('question_view', quiz_id=quiz.id, question_number=question_number+1)
    
    return render(request, 'quiz/question_view.html',{
        'quiz': quiz,
        'question': current_question,
        'answers': answers,
        'question_number': question_number,
        'total_questions': len(questions)
    })

@login_required
def quiz_result_view(request, quiz_id):
    quiz= get_object_or_404(Quiz, id=quiz_id)
    quiz_data = request.session.get('quiz_data',{})
    questions = Question.objects.filter(quiz=quiz)
    correct = 0

    for question in questions:
        selected_answer_id = quiz_data.get(str(question.id))
        if selected_answer_id:
            try:
                answer = Answer.objects.get(id=selected_answer_id)
                if answer.is_correct:
                    correct += 1
            except Answer.DoesNotExist:
                pass
    
    total = question.count()
    score = int((correct/total)*100)

    # save result
    attempt = QuizAttempt.objects.create(
        user = request.user,
        quiz=quiz,
        score=score,
        correct_answers=correct,
        total_questions=total
    )

    # Badge view
    assign_badges(request.user, score,quiz_attempt= attempt)

    # clear session
    request.session['quiz_data'] = {}

    return render( request, 'quiz/quiz_result.html',{
        'quiz':quiz,
        'score':score,
        'correct': correct,
        'total': total
    })


#  Admin Quiz Analytics Dashboard 
@staff_member_required #Restrict access to staff/admin users only

def admin_quiz_analytics(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    # Get filter from URL (?date_filter=weekly)
    date_filter = request.GET.get('date_filter', 'all')  # default: 'all'

    # Determine date range
    if date_filter == 'weekly':
        from_date = now() - timedelta(days=7)
    elif date_filter == 'monthly':
        from_date = now() - timedelta(days=30)
    else:
        from_date = None  #all time, no filtering

    # get all quizattempts, Filter attempts by date if needed
    attempts = QuizAttempt.objects.all()
    if from_date:
        attempts = attempts.filter(date_attempted__gte=from_date)  #calculate toal attempts after filtering

    total_attempts = attempts.count()
    total_badges = UserBadge.objects.count()

    avg_scores = (
        attempts.values('quiz__title')   # group by quiz title
        .annotate(avg_score=Avg('score'))    # calculate avg score
        .order_by('quiz__title')
    )

    user_counts = (
        attempts.values('quiz__title')
        .annotate(user_count=Count('user', distinct=True))    #count unique users 
        .order_by('quiz__title')
    )

    # Extarct chart data for Chart.js
    avg_score_labels = [item['quiz__title'] for item in avg_scores]
    avg_score_data = [item['avg_score'] for item in avg_scores]
    user_count_labels = [item['quiz__title'] for item in user_counts]
    user_count_data = [item['user_count'] for item in user_counts]

    # Send data to HTML template
    context = {
        'total_attempts': total_attempts,
        'total_badges': total_badges,
        'avg_score_labels': json.dumps(avg_score_labels),
        'avg_score_data': json.dumps(avg_score_data),
        'user_count_labels': json.dumps(user_count_labels),
        'user_count_data': json.dumps(user_count_data),
        'selected_filter': date_filter,
    }

    return render(request, 'quiz/admin_quiz_analytics.html', context)