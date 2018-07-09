from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text','fulltext')
        labels = {"text":"Brief description or summary of recipe",
        "fulltext":"Full recipe or instructions (only shown on post detail page)"}

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already being used!')
