from __future__ import annotations

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from materials.models import Material

from .models import Quiz, QuizQuestion
from .services import GeminiError, generate_quiz


class GenerateQuizView(LoginRequiredMixin, View):
    def post(self, request, material_id: int):
        material = get_object_or_404(Material, pk=material_id, owner=request.user)
        question_count = int(request.POST.get("question_count", 5))
        question_count = max(1, min(question_count, 10))
        quiz = Quiz.objects.create(
            owner=request.user,
            material=material,
            status=Quiz.Status.PROCESSING,
            settings={"question_count": question_count},
        )
        redirect_url = reverse('materials:upload') + '#queue'
        try:
            payload = generate_quiz(material, question_count=question_count)
        except GeminiError as exc:
            quiz.status = Quiz.Status.ERROR
            quiz.error_message = str(exc)
            quiz.save(update_fields=["status", "error_message", "updated_at"])
            messages.error(request, f"Quiz generation failed: {exc}")
        else:
            questions = payload.get("questions", [])
            if not questions:
                quiz.status = Quiz.Status.ERROR
                quiz.error_message = 'Gemini did not return any questions.'
                quiz.save(update_fields=['status', 'error_message', 'updated_at'])
                messages.error(request, 'Gemini did not return any questions.')
            else:
                quiz.title = payload.get('quiz_title', material.title or 'Generated Quiz')
                quiz.model_name = getattr(settings, 'GEMINI_MODEL', '')
                quiz.question_count = len(questions)
                quiz.status = Quiz.Status.READY
                quiz.save(update_fields=['title', 'model_name', 'question_count', 'status', 'updated_at'])
                for index, item in enumerate(questions):
                    choices = item.get("choices", [])
                    correct_index = item.get("correct_index", 0)
                    if choices:
                        position = min(max(correct_index, 0), max(len(choices) - 1, 0))
                        correct_answer = choices[position]
                    else:
                        correct_answer = item.get("answer", "")
                    QuizQuestion.objects.create(
                        quiz=quiz,
                        prompt=item.get("prompt", ""),
                        choices=choices,
                        correct_answer=correct_answer,
                        explanation=item.get("explanation", ""),
                        order=index,
                    )
                messages.success(request, "Quiz generated successfully.")
                redirect_url = reverse('quizzes:detail', args=[quiz.pk])
        return redirect(redirect_url)


class QuizListView(LoginRequiredMixin, View):
    template_name = 'quizzes/list.html'

    def get(self, request, material_id: int | None = None):
        quizzes = Quiz.objects.filter(owner=request.user).select_related('material')
        material = None
        if material_id:
            quizzes = quizzes.filter(material_id=material_id)
            material = get_object_or_404(Material, pk=material_id, owner=request.user)
        quizzes = quizzes.order_by('-created_at')
        return render(request, self.template_name, {
            'quizzes': quizzes,
            'material': material,
        })


class QuizDetailView(LoginRequiredMixin, View):
    template_name = 'quizzes/detail.html'

    def get_quiz(self, request, pk: int) -> Quiz:
        return get_object_or_404(
            Quiz.objects.prefetch_related('questions').select_related('material'),
            pk=pk,
            owner=request.user,
        )

    def get(self, request, pk: int):
        quiz = self.get_quiz(request, pk)
        return render(request, self.template_name, {
            'quiz': quiz,
            'questions': quiz.questions.all(),
        })

    def post(self, request, pk: int):
        quiz = self.get_quiz(request, pk)
        questions = quiz.questions.all()
        results = []
        score = 0
        for question in questions:
            field_name = f'q_{question.id}'
            user_answer = request.POST.get(field_name, '').strip()
            correct_answer = (question.correct_answer or '').strip()
            if question.choices:
                is_correct = user_answer == correct_answer
            else:
                is_correct = user_answer.lower() == correct_answer.lower() if user_answer and correct_answer else False
            if is_correct:
                score += 1
            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct': is_correct,
            })
        total = len(questions) or 1
        percent = round((score / total) * 100, 1)
        return render(request, self.template_name, {
            'quiz': quiz,
            'questions': questions,
            'results': results,
            'submitted': True,
            'score': score,
            'total': total,
            'percent': percent,
        })
