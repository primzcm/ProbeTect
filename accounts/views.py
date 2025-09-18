from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import EmailAuthenticationForm, InstructorSignUpForm, StudentSignUpForm
from .models import User


class AuthenticatedRedirectMixin:
    redirect_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):  # type: ignore[override]
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class StudentSignupView(AuthenticatedRedirectMixin, View):
    template_name = "accounts/signup_student.html"
    form_class = StudentSignUpForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
        return render(request, self.template_name, {"form": form})


class InstructorSignupView(StudentSignupView):
    template_name = "accounts/signup_instructor.html"
    form_class = InstructorSignUpForm


class AuthLoginView(AuthenticatedRedirectMixin, LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm


def auth_logout(request):
    """Log the user out and always redirect to the landing page."""
    logout(request)
    return redirect("landing")


class DashboardView(View):
    template_name = "accounts/dashboard.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        role = request.user.role if isinstance(request.user, User) else User.Role.STUDENT
        context = {"role": role}
        return render(request, self.template_name, context)
