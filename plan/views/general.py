from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    # if request.user.is_authenticated:
    #     if request.user.is_teacher:
    #         return redirect('teachers:quiz_change_list')
    #     else:
    #         return redirect('students:quiz_list')
    return render(request, 'general/home.html')


def login(request):
    # if request.user.is_authenticated:
    #     return render(request, 'general/home.html')
    return render(request, 'registration/login.html')
