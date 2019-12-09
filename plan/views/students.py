from datetime import datetime, timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, TemplateView

from ..forms import StudentSignUpForm
from ..models import User, Uczelnie, StudentKierunekSemestr, Studenci, Semestry, PlanyStudentow, PlanyZajecStudentow
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
        return redirect('home')


class StudentEnrolledSemestersListView(TemplateView):
    template_name = 'students/universities_list.html'

    # context_object_name = 'enrolled_semesters'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentEnrolledSemestersListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(StudentEnrolledSemestersListView, self).get_context_data(**kwargs)

        selected_user = Studenci.objects.all().get(user=self.request.user)
        student_semesters = StudentKierunekSemestr.objects.filter(id_studenta=selected_user)
        current_student_semesters = []
        archive_student_semesters = []
        current_plan = {}
        for record in student_semesters:
            try:
                # semestr = Semestry.objects.all().get(pk=record.id_semestru.pk)
                if record.is_current():
                    current_student_semesters.append(record)
                else:
                    archive_student_semesters.append(record)
            except Semestry.DoesNotExist:
                raise
        print(current_student_semesters)

        #  this is very simple, it just needs a genius to understand its simplicity.
        for semester in current_student_semesters:
            if semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni in current_plan:
                if semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu in current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni]:
                    if semester.id_semestru.get_kierunek().nazwa_kierunku in \
                            current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                                semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu]:
                        raise ValueError(
                            "Student nie może studiować jednocześnie tego samego kierunku na różnych semestrach")
                    else:
                        temp_dict = {semester.id_semestru.get_kierunek().nazwa_kierunku: semester}
                        current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                            semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu].update(temp_dict)
                else:
                    current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                        semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu] = {}
                    current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                        semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu][
                        semester.id_semestru.get_kierunek().nazwa_kierunku] = semester
            else:
                current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni] = {}
                current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                    semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu] = {}
                current_plan[semester.id_semestru.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                    semester.id_semestru.get_kierunek().get_wydzial().nazwa_wydzialu][
                    semester.id_semestru.get_kierunek().nazwa_kierunku] = semester
        context['current_plan'] = current_plan
        return context


class StudentTimeScheduleView(TemplateView):
    template_name = "students/../../templates/students/timetable.html"
    time = ""
    day_of_week = ""
    semester = ""
    selected_student = ""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.time = kwargs.get('time', datetime.now)
        self.semester = kwargs.get('semester', None)
        self.day_of_week = kwargs.get('week_day', None)
        return super(StudentTimeScheduleView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(StudentTimeScheduleView, self).get_context_data(**kwargs)
        dt = datetime.strptime(self.time, "%d-%m-%Y")
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        week_dmy = [datetime.strftime(start + timedelta(days=x), "%d-%m-%Y") for x in range(0, (end - start).days + 1)]
        next_week = dt + timedelta(days=7)
        next_week = datetime.strftime(next_week, "%d-%m-%Y")
        last_week = dt - timedelta(days=7)
        last_week = datetime.strftime(last_week, "%d-%m-%Y")

        semester = StudentKierunekSemestr.objects.all().get(pk=self.semester)
        plan = PlanyStudentow.objects.all().get(id_semestru=semester.id_semestru, nr_albumu=semester.id_studenta)
        all_plans = PlanyZajecStudentow.objects.all().filter(id_planu=plan, id_sali__data_rozpoczecia__gte=start,
                                                             id_sali__data_zakonczenia__lte=end)
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
        context['semester'] = self.semester
        context['all_plans'] = all_plans
        return context


class StudentsListView(ListView):
    template_name = 'students/students_list.html'
    model = StudentKierunekSemestr

    # We are only interested in students who study in the users faculties the same major
    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                student = Studenci.objects.all().get(user=self.request.user)
                semestry_studenta = StudentKierunekSemestr.objects.all().filter(id_studenta=student).values(
                    'id_semestru')
                semestry = Semestry.objects.all().filter(id_semestru__in=semestry_studenta)
                studenci = StudentKierunekSemestr.objects.all().filter(
                    Q(id_semestru__in=semestry) & ~Q(id_studenta=student))
                return studenci
        else:
            return None
