from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment

class registration_form(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(registration_form, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class log_in_form(AuthenticationForm):
    username=forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={
            'name':'username'
        })
    )
    password=forms.CharField(
        label="Password",
        max_length=32,
        widget=forms.PasswordInput()
        )
# class edit_form(ModelForm):
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#     email = forms.EmailField(required=False)
#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "email")
#     #TODO: the rest
    #https://stackoverflow.com/questions/22567320/django-edit-user-profile

# class comment_form(forms.Form):
#     comment = forms.CharField(label='Suggestion', max_length=140)
#
#     def save(self, request , commit=True):
#         com = comment()
#         com.comment = self.cleaned_data['comment']
#         suggest.author = request.user
#         if commit:
#             com.save()
#         return com
#
# class reply_form(forms.Form):
#     reply = forms.CharField(
#         label='Reply',
#         max_length=140,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Add a reply'}
#         )
#     )

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
