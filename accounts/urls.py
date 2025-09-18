from django.urls import path

from .views import (
    AuthLoginView,
    AuthLogoutView,
    DashboardView,
    InstructorSignupView,
    StudentSignupView,
)

urlpatterns = [
    path("login/", AuthLoginView.as_view(), name="login"),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
    path("signup/student/", StudentSignupView.as_view(), name="signup_student"),
    path("signup/instructor/", InstructorSignupView.as_view(), name="signup_instructor"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
