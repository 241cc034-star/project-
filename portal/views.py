
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'portal/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'portal/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'portal/dashboard.html')


@login_required
def upload_paper(request):
    return render(request, 'portal/upload.html')


@login_required
def reviewer_dashboard(request):
    return render(request, 'portal/reviewer_dashboard.html')


@login_required
def review_paper(request, paper_id):
    return render(
        request,
        'portal/review.html',
        {'paper_id': paper_id}
    )


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('dashboard')