from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html",
             email_template_name="accounts/password_reset_email.txt",
             success_url="/account/password-reset/sent/",
         ),
         name="password_reset"),
    path("password-reset/sent/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_done.html",
         ),
         name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html",
             success_url="/account/password-reset/complete/",
         ),
         name="password_reset_confirm"),
    path("password-reset/complete/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_complete.html",
         ),
         name="password_reset_complete"),
]
