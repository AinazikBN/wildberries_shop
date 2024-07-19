from django.shortcuts import render
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .import views
from django.http import HttpResponse
from django.core.mail import send_mail

def test_email_view(request):
    send_mail(
        'Test Email',
        'This is a test email.',
        'adacorp@gmail.com',
        ['recipient@example.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent")

app_name = 'account'
 
urlpatterns = [
    # registration and verification 
    path('register/', views.register_user, name='register'), 
    path('email-verification-sent/',
          lambda request: render(request, 'account/email/email-verification-sent.html'), 
          name='email-verification-sent' ), 

    # Login and dashbord
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    
    path('dashboard/', views.dashboard_user, name='dashboard'), 
    path('profile-management/', views.profile_user, name='profile-management'), 
    path('delete-user/', views.delete_user, name='delete-user'),
    
    #Password reset 
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="account/password/password-reset.html",
        email_template_name="account/password/password_reset_email.html",
        success_url=reverse_lazy("account:password_reset_done"),
    ),
    name="password-reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-confirm.html",
            success_url=reverse_lazy("account:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path('test-email/', test_email_view, name='test_email'),

]

