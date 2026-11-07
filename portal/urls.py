
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Registration
    path('register/', views.register_view, name='register'),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='portal/login.html'
        ),
        name='login'
    ),

    # Student Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Upload Paper
    path('upload/', views.upload_paper, name='upload'),

    # Reviewer Dashboard
    path(
        'reviewer/',
        views.reviewer_dashboard,
        name='reviewer_dashboard'
    ),

    # Review Paper
    path(
        'review/<int:paper_id>/',
        views.review_paper,
        name='review'
    ),

    # Activate Reviewer Account
    path(
        'make-reviewer/',
        views.make_arun_reviewer,
        name='make_arun_reviewer'
    ),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]
