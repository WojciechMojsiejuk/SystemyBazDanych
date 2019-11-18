from django.urls import include, path

from .views import general, students, teachers

urlpatterns = [
    path('home/', general.home, name='home'),
    path('students/', include(([
                                   path('', students.StudentEnrolledSemestersListView.as_view(),
                                        name='universities_list'),
                                   path('', students.StudentEnrollInSemesterView.as_view(),
                                        name='new_enroll'),

                               ], 'plan'), namespace='students')),
]
