from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import CustomUser, Post, Report, UserPreference
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'contact_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Set to inactive until admin approves
        if commit:
            user.save()
        return user

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['message']

    def __init__(self, *args, **kwargs):
        self.reported_user = kwargs.pop('reported_user', None)
        self.reported_post = kwargs.pop('reported_post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        report = super().save(commit=False)
        report.reported_user = self.reported_user
        report.reported_post = self.reported_post
        if commit:
            report.save()
        return report

