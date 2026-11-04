
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Paper


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class PaperForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = [
            'title',
            'abstract',
            'paper_file'
        ]

    def clean_paper_file(self):
        file = self.cleaned_data.get('paper_file')

        if file and not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError(
                'Only PDF files are allowed.'
            )

        if file and file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                'Maximum file size is 10 MB.'
            )

        return file