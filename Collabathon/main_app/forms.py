from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Comment

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    newsLetter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'newsLetter')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EditForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']