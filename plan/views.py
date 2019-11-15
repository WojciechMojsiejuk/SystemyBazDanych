from django.contrib.auth import login, authenticate
from .forms import SignUpFormStudent, SignUpFormTeacher
from django.shortcuts import render, redirect

# Create your views here.
def signupstudent(request):
    if request.method == 'POST':
        form = SignUpFormStudent(request.POST)
        if form.is_valid():
            form.save()
            pesel = form.cleaned_data.get('pesel')
            haslo = form.cleaned_data.get('password1')
            imie = form.cleaned_data.get('imie')
            nazwisko = form.cleaned_data.get('nazwisko')
    else:
        form = SignUpFormStudent()
    return render(request, 'signup.html', {'form': form})


def signupteacher(request):
    if request.method == 'POST':
        form = SignUpFormTeacher(request.POST)
        if form.is_valid():
            form.save()
            pesel = form.cleaned_data.get('pesel')
            haslo = form.cleaned_data.get('password1')
            imie = form.cleaned_data.get('imie')
            nazwisko = form.cleaned_data.get('nazwisko')
    else:
        form = SignUpFormTeacher()
    return render(request, 'signup.html', {'form': form})
