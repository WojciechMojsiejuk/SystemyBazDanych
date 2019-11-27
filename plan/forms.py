from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from plan.models import Studenci, User, Nauczyciele, StudentKierunekSemestr, Kierunki, Semestry


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


class StudentEnrollInSemesterForm(forms.ModelForm):
    # ToDo: Dokończyć formularz zapisu studenta na kierunki
    class Meta:
        model = StudentKierunekSemestr
        fields = ('id_studenta', 'id_semestru', 'data_rozpoczecia', 'data_zakonczenia')
    # id_kierunku = forms.ModelChoiceField(queryset=Kierunki.objects.all())
    # id_semestru = forms.ModelChoiceField(queryset=Semestry.objects.filter(id_kierunku=id_kierunku))
    pass