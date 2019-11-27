from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('students:universities_list')
        elif request.user.is_student:
            return redirect('students:universities_list')
    return render(request, 'general/home.html')


def login(request):
    if request.user.is_authenticated:
        return render(request, 'general/home.html')
    return render(request, 'registration/login.html')


class RoomsListView(ListView):
    template_name = 'general/rooms_list.html'
    pass
