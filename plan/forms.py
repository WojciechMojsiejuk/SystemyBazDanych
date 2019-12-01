from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import Form

from plan.models import Studenci, User, Nauczyciele, StudentKierunekSemestr, Kierunki, Semestry, ZajetoscSal, Sale


class StudentSignUpForm(UserCreationForm):

    imie = forms.CharField(max_length=100, required=True)
    nazwisko = forms.CharField(max_length=100, required=True)
    pesel = forms.CharField(max_length=11, required=True, help_text="PESEL number consists of 11 digits")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Studenci.objects.create(
            user=user,
            imie=self.cleaned_data.get('imie'),
            nazwisko=self.cleaned_data.get('nazwisko'),
            pesel=self.cleaned_data.get('pesel')
        )
        return user


class TeacherSignUpForm(UserCreationForm):

    imie = forms.CharField(max_length=100, required=True)
    nazwisko = forms.CharField(max_length=100, required=True)
    pesel = forms.CharField(max_length=11, required=True, help_text="PESEL number consists of 11 digits")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Nauczyciele.objects.create(
            user=user,
            imie=self.cleaned_data.get('imie'),
            nazwisko=self.cleaned_data.get('nazwisko'),
            pesel=self.cleaned_data.get('pesel')

        )
        return user

#
# class ReservationCreateForm(Form):
#     data_rozpoczecia = forms.DateTimeField()
#     data_zakonczenia = forms.DateTimeField()
#
#     class Meta:
#         model = ZajetoscSal
