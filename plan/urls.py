from datetime import datetime

from django.urls import include, path

from .views import general, students, teachers

urlpatterns = [

    path('', general.home, name='home'),
    path('home/', general.home, name='home'),
    path('students/', include(([
                                   path('', students.StudentEnrolledSemestersListView.as_view(),
                                        name='universities_list'),
                                   path('timetable/<str:semester>/<str:time>/<str:week_day>', students.StudentTimeScheduleView.as_view(),
                                        name='show_timetable'),

                               ], 'plan'), namespace='students')),
]
