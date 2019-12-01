from django.db.models import Q
from django.shortcuts import render
from django.views import View

from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta

from plan.models import Nauczyciele, StudentKierunekSemestr, Studenci, Semestry, MiejscaZatrudnienia, Sale, Wydziały, \
    ZajetoscSal, PlanyNauczycieli, PlanyZajecStudentow, PrzedmiotyNauczycieli, Przedmioty, PlanyStudentow


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
        teacher = None
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                student = Studenci.objects.all().get(user=self.request.user)
                semestry_studenta = StudentKierunekSemestr.objects.all().filter(id_studenta=student).values('id_semestru')
                semestry = Semestry.objects.all().filter(id_semestru__in=semestry_studenta)
                for semestr in semestry:
                    wydziały.append(semestr.get_kierunek().get_wydzial())
                wydziały = list(set(wydziały))
            if self.request.user.is_teacher:
                teacher = Nauczyciele.objects.all().get(user=self.request.user)
                wydziały = MiejscaZatrudnienia.objects.all().filter(id_nauczyciela=teacher).values('id_wydzialu')
            nauczyciele = MiejscaZatrudnienia.objects.all().filter(id_wydzialu__in=wydziały).values('id_nauczyciela')
            return Nauczyciele.objects.all().filter(Q(user__in=nauczyciele) & ~Q(user=teacher))
        else:
            return None


class RoomsListView(ListView):
    template_name = 'general/rooms_list.html'
    model = Sale

    def get_queryset(self):
        if self.request.user.is_authenticated:
            wydziały = []
            if self.request.user.is_teacher:
                nauczyciel = Nauczyciele.objects.all().get(user=self.request.user)
                wydziały = MiejscaZatrudnienia.objects.all().filter(id_nauczyciela=nauczyciel).values('id_wydzialu')
            elif self.request.user.is_student:
                student = Studenci.objects.all().get(user=self.request.user)
                semestry_studenta = StudentKierunekSemestr.objects.all().filter(id_studenta=student).values("id_semestru")
                semestry = Semestry.objects.all().filter(id_semestru__in=semestry_studenta)
                for semestr in semestry:
                    wydziały.append(semestr.get_kierunek().get_wydzial())
                wydziały = list(set(wydziały))
            sale = Sale.objects.all().filter(id_wydzialu__in=wydziały)
            return sale
        else:
            return None


class RoomsAvailabilityView(TemplateView):
    template_name = 'general/timetable.html'
    date = ""
    day_of_week = ""
    room = ""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.date = kwargs.get('date', datetime.now)
        self.day_of_week = kwargs.get('week_day', None)
        self.room = kwargs.get('room', None)
        return super(RoomsAvailabilityView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(RoomsAvailabilityView, self).get_context_data(**kwargs)
        dt = datetime.strptime(self.date, "%d-%m-%Y")
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        week_dmy = [datetime.strftime(start + timedelta(days=x), "%d-%m-%Y") for x in range(0, (end - start).days+1)]
        next_week = dt + timedelta(days=7)
        next_week = datetime.strftime(next_week, "%d-%m-%Y")
        last_week = dt - timedelta(days=7)
        last_week = datetime.strftime(last_week, "%d-%m-%Y")

        room = Sale.objects.all().get(id_sali=self.room)
        booked = ZajetoscSal.objects.all().filter(id_sali=room, data_rozpoczecia__gte=start, data_zakonczenia__lte=end)

        teacher_plans = None
        students_plans = None
        teacher_subjects = None
        if self.request.user.is_teacher:
            teacher = Nauczyciele.objects.all().get(user=self.request.user)
            teacher_plans = PlanyNauczycieli.objects.all().filter(id_nauczyciela=teacher)
            students_plan_list = PlanyZajecStudentow.objects.all().filter(id_nauczyciela=teacher).values("id_planu")
            students_plans = list(set(PlanyStudentow.objects.all().filter(id_planu__in=students_plan_list)))
            teacher_subjects_list = PrzedmiotyNauczycieli.objects.all().filter(id_nauczyciela=teacher).values("id_przedmiotu")
            teacher_subjects = Przedmioty.objects.all().filter(id_przedmiotu__in=teacher_subjects_list)
        print(students_plans)
        context['students_plans'] = students_plans
        context['teacher_plans'] = teacher_plans
        context['teacher_subjects'] = teacher_subjects
        context['time'] = dt
        context['week_start'] = start
        context['week_end'] = end
        context['monday'] = week_dmy[0]
        context['tuesday'] = week_dmy[1]
        context['wednesday'] = week_dmy[2]
        context['thursday'] = week_dmy[3]
        context['friday'] = week_dmy[4]
        context['saturday'] = week_dmy[5]
        context['sunday'] = week_dmy[6]
        context['next_week'] = next_week
        context['last_week'] = last_week
        context['day_of_week'] = self.day_of_week
        context['room'] = room
        context['booked'] = booked
        return context


class ReservationCreateView(View):
    pass

