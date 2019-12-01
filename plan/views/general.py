from django.db.models import Q
from django.shortcuts import redirect, render

from django.views.generic import TemplateView, ListView

from plan.models import Nauczyciele, StudentKierunekSemestr, Studenci, Semestry, MiejscaZatrudnienia


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class HomeView(TemplateView):
    template_name = 'general/home.html'

    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HomeView, self).get_context_data(**kwargs)
        degra_user = None
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                degra_user = Studenci.objects.all().get(user=self.request.user)
            elif self.request.user.is_teacher:
                degra_user = Nauczyciele.objects.all().get(user=self.request.user)
        context['degra_user'] = degra_user
        return context


def login(request):
    if request.user.is_authenticated:
        return render(request, 'general/home.html')
    return render(request, 'registration/login.html')


class TeachersListView(ListView):
    template_name = 'general/teachers_list.html'
    model = Nauczyciele

    def get_queryset(self):
        # We are only interested in teachers who teach in the same faculty in which user is studying or working
        wydziały = []
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                student = Studenci.objects.all().get(user=self.request.user)
                semestry_studenta = StudentKierunekSemestr.objects.all().filter(id_studenta=student).values('id_semestru')
                semestry = Semestry.objects.all().filter(id_semestru__in=semestry_studenta)
                for semestr in semestry:
                    wydziały.append(semestr.get_kierunek().get_wydzial())
            if self.request.user.is_teacher:
                teacher = Nauczyciele.objects.all().get(user=self.request.user)
                wydziały = MiejscaZatrudnienia.objects.all().filter(id_nauczyciela=teacher).values('id_wydzialu')
                print(teacher)
                print(wydziały)
            nauczyciele = MiejscaZatrudnienia.objects.all().filter(id_wydzialu__in=wydziały).values('id_nauczyciela')
            return Nauczyciele.objects.all().filter(Q(user__in=nauczyciele) & ~Q(user=teacher))
        else:
            return None


class RoomsListView(ListView):
    template_name = 'general/rooms_list.html'
    pass





