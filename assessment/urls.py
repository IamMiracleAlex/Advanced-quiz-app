from django.urls import include, path
from assessment import views

app_name = 'assessments'

urlpatterns = [
    path('assessments/', views.QuizListView.as_view(), name='quiz_list'),
    path('assessments/taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('assessments/quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    # path("test/", views.test, name="test")
]
