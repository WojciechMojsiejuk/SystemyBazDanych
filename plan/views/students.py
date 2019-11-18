from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView

from ..forms import StudentSignUpForm, StudentEnrollInSemesterForm
from ..models import User, Uczelnie, StudentKierunekSemestr, Studenci
from django.utils.decorators import method_decorator


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('signup')


class StudentEnrolledSemestersListView(ListView):

    template_name = 'students/universities_list.html'
    context_object_name = 'enrolled_semesters'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentEnrolledSemestersListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        selected_user = Studenci.objects.all().get(user=self.request.user)
        return StudentKierunekSemestr(id_studenta=selected_user)


class StudentEnrollInSemesterView(CreateView):
    model = StudentKierunekSemestr
    form_class = StudentEnrollInSemesterForm
