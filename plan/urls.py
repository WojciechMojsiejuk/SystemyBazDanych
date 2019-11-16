
from django.urls import include, path

from .views import general, students, teachers

urlpatterns = [
    path('home/', general.home, name='home'),
    ]