from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput

User = get_user_model()

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your email Address'
        self.fields['email'].required = True
          

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() or len(email) > 254:
            raise forms.ValidationError('Email is already in  use')
        
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your email address'
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() or len(email) > 254:
            raise forms.ValidationError('Email is already in use')
        
        return email
    
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']


