from django.contrib import admin

from .models import Quiz, QuizQuestion


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "material", "status", "question_count", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "owner__username", "material__title")
    readonly_fields = ("created_at", "updated_at", "question_count", "model_name", "status")
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "order", "prompt", "correct_answer")
    list_filter = ("quiz",)
    search_fields = ("prompt", "correct_answer")
