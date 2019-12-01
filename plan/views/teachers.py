from datetime import datetime, timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from ..forms import TeacherSignUpForm
from ..models import User, PlanyNauczycieli, Nauczyciele, PlanyZajecNauczycieli


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class TeacherTimeScheduleView(TemplateView):
    template_name = "teachers/../../templates/teachers/timetable.html"
    time = ""
    day_of_week = ""
    teacher = ""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.time = kwargs.get('time', datetime.now)
        self.teacher = kwargs.get('teacher', None)
        self.day_of_week = kwargs.get('week_day', None)
        return super(TeacherTimeScheduleView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TeacherTimeScheduleView, self).get_context_data(**kwargs)
        dt = datetime.strptime(self.time, "%d-%m-%Y")
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        week_dmy = [datetime.strftime(start + timedelta(days=x), "%d-%m-%Y") for x in range(0, (end - start).days+1)]
        next_week = dt + timedelta(days=7)
        next_week = datetime.strftime(next_week, "%d-%m-%Y")
        last_week = dt - timedelta(days=7)
        last_week = datetime.strftime(last_week, "%d-%m-%Y")

        nauczyciel = Nauczyciele.objects.all().get(user=self.teacher)
        plan = PlanyNauczycieli.objects.all().filter(id_nauczyciela=nauczyciel)
        all_plans = PlanyZajecNauczycieli.objects.all().filter(id_planu__in=plan, id_sali__data_rozpoczecia__gte=start, id_sali__data_zakonczenia__lte=end)
        print(all_plans)
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
        context['teacher'] = self.teacher
        context['all_plans'] = all_plans
        return context
