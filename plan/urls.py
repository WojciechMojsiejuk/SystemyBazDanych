from django.urls import include, path

from .views import general, students, teachers

urlpatterns = [
    path('home/', general.home, name='home'),
    path('students/', include(([
                                   path('', students.StudentEnrolledSemestersListView.as_view(),
                                        name='universities_list'),
                                   path('Enroll', students.StudentEnrollInSemesterView.as_view(),
                                        name='new_enroll'),
                                   path('timetable', students.StudentTimeScheduleView.as_view(),
                                        name='show_timetable'),

                               ], 'plan'), namespace='students')),
]
