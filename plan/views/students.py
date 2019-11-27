from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, TemplateView

from ..forms import StudentSignUpForm, StudentEnrollInSemesterForm
from ..models import User, Uczelnie, StudentKierunekSemestr, Studenci, Semestry
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
        print("Selected user")
        print(selected_user)
        student_semesters = StudentKierunekSemestr.objects.filter(id_studenta=selected_user)
        print("Students semester")
        print(student_semesters)
        current_student_semesters = []
        archive_student_semesters = []
        current_plan = {}
        for record in student_semesters:
            try:
                semestr = Semestry.objects.all().get(pk=record.id_semestru.pk)
                if record.is_current():
                    current_student_semesters.append(semestr)
                else:
                    archive_student_semesters.append(semestr)
            except Semestry.DoesNotExist:
                raise
        print("curent semesters")
        print(current_student_semesters)

        #  this is very simple, it just needs a genius to understand its simplicity.
        print("current plan")
        for semester in current_student_semesters:
            if semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni in current_plan:
                print(semester.get_kierunek().get_wydzial().nazwa_wydzialu)
                if semester.get_kierunek().get_wydzial().nazwa_wydzialu in current_plan[
                    semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni]:
                    if semester.get_kierunek().nazwa_kierunku in \
                            current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                                semester.get_kierunek().get_wydzial().nazwa_wydzialu]:
                        raise ValueError(
                            "Student nie może studiować jednocześnie tego samego kierunku na różnych semestrach")
                    else:
                        temp_dict = {semester.get_kierunek().nazwa_kierunku: semester.nr_semestru}
                        current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                            semester.get_kierunek().get_wydzial().nazwa_wydzialu].update(temp_dict)
                else:
                    current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                        semester.get_kierunek().get_wydzial().nazwa_wydzialu] = {}
                    current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                        semester.get_kierunek().get_wydzial().nazwa_wydzialu][
                        semester.get_kierunek().nazwa_kierunku] = semester.nr_semestru
            else:
                current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni] = {}
                current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                    semester.get_kierunek().get_wydzial().nazwa_wydzialu] = {}
                current_plan[semester.get_kierunek().get_wydzial().get_uczelnia().nazwa_uczelni][
                    semester.get_kierunek().get_wydzial().nazwa_wydzialu][
                    semester.get_kierunek().nazwa_kierunku] = semester.nr_semestru
            print(current_plan)

        print("final current plan")
        print(current_plan)

        context['current_plan'] = current_plan
        return context


class StudentEnrollInSemesterView(CreateView):
    model = StudentKierunekSemestr
    form_class = StudentEnrollInSemesterForm


class StudentTimeScheduleView(TemplateView):
    template_name = "general/timetable.html"

