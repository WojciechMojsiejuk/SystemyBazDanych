from datetime import datetime

from django.urls import include, path

from .views import general, students, teachers

urlpatterns = [

    path('', general.HomeView.as_view(), name='home'),
    path('home/', general.HomeView.as_view(), name='home'),
    path('students/', include(([
                                   path('', students.StudentEnrolledSemestersListView.as_view(),
                                        name='universities_list'),
                                   path('timetable/<str:semester>/<str:time>/<str:week_day>', students.StudentTimeScheduleView.as_view(),
                                        name='show_timetable'),
                                   path('students_plans', students.StudentsListView.as_view(),
                                        name='students_list'),

                               ], 'plan'), namespace='students')),
    path('teachers/', include(([
                                   path('teachers_plans', general.TeachersListView.as_view(),
                                        name='teachers_list'),
                                   path('timetable/<str:teacher>/<str:time>/<str:week_day>', teachers.TeacherTimeScheduleView.as_view(),
                                        name='teacher_timetable'),
                               ], 'plan'), namespace='teachers')),
    path('room_availability/', include(([
                                    path('', general.RoomsListView.as_view(),
                                        name='room_availability'),
                                    path('<str:room>/<str:date>/<str:week_day>', general.RoomsAvailabilityView.as_view(),
                                        name='booked_rooms'),
                                ], 'rooms'), namespace='rooms')),
]
