from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Uczelnie)
admin.site.register(Wydziały)
admin.site.register(Kierunki)
admin.site.register(Semestry)
admin.site.register(Studenci)
admin.site.register(Nauczyciele)
admin.site.register(Sale)
admin.site.register(ZajetoscSal)
admin.site.register(PlanyStudentow)
admin.site.register(PlanyNauczycieli)
admin.site.register(Przedmioty)
admin.site.register(PrzedmiotyNauczycieli)
admin.site.register(PrzedmiotyWSemestrze)
admin.site.register(MiejscaZatrudnienia)
admin.site.register(PlanyZajecStudentow)
admin.site.register(PlanyZajecNauczycieli)
admin.site.register(StudentKierunekSemestr)