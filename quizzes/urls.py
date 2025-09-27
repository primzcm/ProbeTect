from django.urls import path

from .views import GenerateQuizView, QuizDetailView, QuizListView

app_name = 'quizzes'

urlpatterns = [
    path('materials/<int:material_id>/generate/', GenerateQuizView.as_view(), name='generate'),
    path('materials/<int:material_id>/', QuizListView.as_view(), name='list_by_material'),
    path('<int:pk>/', QuizDetailView.as_view(), name='detail'),
    path('', QuizListView.as_view(), name='list'),
]
