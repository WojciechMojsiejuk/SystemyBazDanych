from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView

from plan.models import Nauczyciele, StudentKierunekSemestr, Studenci, Semestry, MiejscaZatrudnienia, Sale, Wydziały


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
            nauczyciele = MiejscaZatrudnienia.objects.all().filter(id_wydzialu__in=list(set(wydziały))).values('id_nauczyciela')
            return Nauczyciele.objects.all().filter(user__in=nauczyciele)
        else:
            return None


class RoomsListView(ListView):
    template_name = 'general/rooms_list.html'
    model = Sale

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_teacher:
                nauczyciel = Nauczyciele.objects.all().get(user=self.request.user)
                wydzial_nauczyciela = MiejscaZatrudnienia.objects.all().filter(id_nauczyciela=nauczyciel).values('id_wydzialu')
                #wydzial = Wydziały.objects.all().filter(id_wydzialu = wydzial_nauczyciela)
                return Sale.objects.all().filter(id_wydzialu=wydzial_nauczyciela)
        else:
            return None

    #pass
