
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='portal/login.html'
        ),
        name='login'
    ),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_paper, name='upload'),

    path(
        'reviewer/',
        views.reviewer_dashboard,
        name='reviewer_dashboard'
    ),

    path(
        'review/<int:paper_id>/',
        views.review_paper,
        name='review'
    ),

    path('logout/', views.logout_view, name='logout'),
]