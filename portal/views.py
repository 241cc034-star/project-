
import os
import secrets

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from .models import Paper
from .forms import RegisterForm, PaperForm


# Home Page
def home(request):
    return render(request, 'portal/home.html')


# User Registration
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'portal/register.html', {'form': form})


# Student Dashboard
@login_required
def dashboard(request):
    papers = Paper.objects.filter(
        uploaded_by=request.user
    ).order_by('-uploaded_at')

    return render(
        request,
        'portal/dashboard.html',
        {'papers': papers}
    )


# Upload Research Paper
@login_required
def upload_paper(request):
    if request.method == 'POST':
        form = PaperForm(request.POST, request.FILES)

        if form.is_valid():
            paper = form.save(commit=False)
            paper.uploaded_by = request.user
            paper.save()

            messages.success(
                request,
                'Research paper uploaded successfully!'
            )
            return redirect('dashboard')
    else:
        form = PaperForm()

    return render(
        request,
        'portal/upload.html',
        {'form': form}
    )


# Reviewer Permission Check
def is_reviewer(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


# Reviewer Dashboard
@login_required
@user_passes_test(is_reviewer)
def reviewer_dashboard(request):
    papers = Paper.objects.all().order_by('-uploaded_at')

    return render(
        request,
        'portal/reviewer_dashboard.html',
        {'papers': papers}
    )


# Review Paper and Submit Feedback
@login_required
@user_passes_test(is_reviewer)
def review_paper(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)

    if request.method == 'POST':
        feedback = request.POST.get(
            'reviewer_feedback', ''
        ).strip()

        status = request.POST.get('status', '')

        allowed_statuses = [
            choice[0] for choice in Paper.STATUS_CHOICES
        ]

        if status not in allowed_statuses:
            messages.error(request, 'Invalid paper status.')

        else:
            paper.reviewer_feedback = feedback
            paper.status = status
            paper.reviewed_by = request.user
            paper.reviewed_at = timezone.now()
            paper.save()

            messages.success(
                request,
                'Review feedback saved successfully!'
            )
            return redirect('reviewer_dashboard')

    return render(
        request,
        'portal/review.html',
        {'paper': paper}
    )


# Secure Reviewer Activation for arun
@login_required
def make_arun_reviewer(request):

    if request.method != 'POST':
        return render(request, 'portal/make_reviewer.html')

    # Only the arun account can activate itself
    if request.user.username != 'arun':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    submitted_token = request.POST.get('token', '')
    saved_token = os.environ.get('BOOTSTRAP_REVIEWER_TOKEN', '')

    if not saved_token or not secrets.compare_digest(
        submitted_token, saved_token
    ):
        messages.error(request, 'Invalid security token.')
        return redirect('make_arun_reviewer')

    request.user.is_staff = True
    request.user.save(update_fields=['is_staff'])

    messages.success(
        request,
        'Reviewer access enabled successfully!'
    )

    return redirect('reviewer_dashboard')


# Logout
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('home')

    return redirect('dashboard')
