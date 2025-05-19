from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import CustomUser, Task

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_image')

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        help_text='Upload a CSV file'
    )

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user', 'csv_data', 'image']
        widgets = {
            'csv_data': forms.HiddenInput(),
        }

class NoteForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3})) 