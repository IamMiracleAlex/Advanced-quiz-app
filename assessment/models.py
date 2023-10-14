from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe


User = get_user_model()


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes', verbose_name='Author')
    name = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    time = models.IntegerField(verbose_name='Time Allocated', default=0, help_text='Specify time in minutes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Quiz'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Question')

    def __str__(self):
        return mark_safe(self.text[:100])


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(verbose_name='Answer', max_length=255)
    is_correct = models.BooleanField(verbose_name='Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='students')
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('id')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Taken Quiz Records'



class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name_plural = 'Student Answers'


    def __str__(self):
        return f'{self.student} chose "{self.answer}" '  