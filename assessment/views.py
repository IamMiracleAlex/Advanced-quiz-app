from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import TakeQuizForm
from .models import Quiz, Student, TakenQuiz, User
from assessment.utils import send_failed_test_email, send_passed_test_email
from app.models import PersonalInfo



# def test(request):
#     return render(request, 'app/test_successful.html')


@method_decorator([login_required, ], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'assessment/quiz_lists.html'

    def get_queryset(self):
        
        queryset = Quiz.objects.filter(published=True) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'assessment/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.students.taken_quizzes \
            .select_related('quiz', 'quiz__owner') \
            .order_by('quiz__name')
        return queryset


@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.students
   
    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'assessment/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    question = unanswered_questions.first()

    if request.GET.get('time_up', None):
        return record_quiz(request=request,
                    quiz=quiz,
                    total_questions=total_questions,
                    student=student)          


    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():

                    return handle_quiz(request, pk)
                    # return redirect('assessments:handle_quiz', pk) #here
                else:
                    
                    return record_quiz(request=request,
                                        quiz=quiz,
                                        total_questions=total_questions,
                                        student=student)
        else:

            context = {
                'form': form,
                'quiz': quiz,
                'question': question,
            }
            html_form = render_to_string('assessment/partials/quiz_form.html',
            context,
            request=request,
            )
            return JsonResponse({'html_form':html_form})




            
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'assessment/take_the_quiz.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
    })


def handle_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.students

    unanswered_questions = student.get_unanswered_questions(quiz)
    question = unanswered_questions.first()
    form = TakeQuizForm(question=question)

    context = {'form': form,
                'quiz': quiz,
                'question': question,
            }
    html_form = render_to_string('assessment/partials/quiz_form.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form':html_form})


def record_quiz(request, quiz, total_questions, student):
    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
    score = round((correct_answers / total_questions) * 100.0, 2)
    profile = PersonalInfo.objects.get(user=request.user)
    TakenQuiz.objects.create(student=student, quiz=quiz, score=score, email=profile.email_address, phone=profile.phone)
    profile.taken_test = True
    profile.save()
    # profile.update(taken_test = True)
    
    if score < 40.0:
        send_failed_test_email(profile)
    else:
        send_passed_test_email(profile)
    html_form = render_to_string('assessment/test_successful.html',
        request=request,
    )
    return JsonResponse({'html_form': html_form, 'recorded':True})