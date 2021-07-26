from django import forms
from django.contrib.auth.models import User
from .models import UserClass

class Register(forms.ModelForm):
    classifier = [('is_student', 'Student'), ('is_teacher', 'Teacher')]
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
        
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retype Password', widget=forms.PasswordInput)
    usertype = forms.ChoiceField(choices=classifier)
    
    def verify_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if len(password1) < 6 or len(password2) < 6:
            raise forms.ValidationError('Password must be at least six characters long')
            return None
        
        elif password1 != password2:
            raise forms.ValidationError('Passwords do not match')
            return None
        
        else:
            return self.password1
    
class UserClassName(forms.ModelForm):
    class Meta:
        model = UserClass
        fields = ['Class']