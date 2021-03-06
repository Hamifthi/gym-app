from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='sign-up'),
    path('register/athlete/', views.AthleteRegister.as_view(), name='register_athlete'),
    path('register/coach/', views.CoachRegister.as_view(), name='register_coach'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/',
        auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
        name='change_password'
    ),
    path('reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='reset_password.html',
            success_url=reverse_lazy('reset_password_done'),
            subject_template_name='reset_password_subject.txt',
            email_template_name='reset_password_email.html'
            ),
        name='reset_password'
    ),
    path('reset_password/done',
        auth_views.PasswordResetDoneView.as_view(template_name='reset_password_done.html'),
        name='reset_password_done'
    ),
    re_path('reset_password/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='reset_password_confirm.html',
            success_url=reverse_lazy('reset_password_complete')
            ),
        name='reset_password_confirm'
    ),
    path('reset_password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='reset_password_complete.html'
            ),
        name='reset_password_complete'
    ),
]