from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Studenci, Nauczyciele


class SignUpFormStudent(UserCreationForm):
    login = False

    class Meta:
        model = Studenci
        fields = ('pesel', 'imie', 'nazwisko' ,'password1', 'password2')
        labels = {
            'pesel' : 'Numer PESEL',
        }

    # def __init__(self, *args, **kwargs):
    #     super(SignUpForm, self).__init__(*args, **kwargs)
    #     self.fields['pesel'].help_text = 'Podaj PESEL'
    #     self.fields['nr_albumu'].help_text = 'Podaj numer albumu? XD'
    #     self.fields['haslo'].help_text = 'Podaj hasło'

class SignUpFormTeacher(UserCreationForm):
    login = False

    class Meta:
        model = Nauczyciele
        fields = ('pesel', 'imie', 'nazwisko' ,'password1', 'password2')
        labels = {
            'pesel' : 'Numer PESEL',
        }
