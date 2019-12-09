import datetime

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Uczelnie(models.Model):
    nazwa_uczelni = models.CharField(max_length=100, primary_key=True)
    adres_uczelni = models.TextField()

    def __str__(self):
        return str(self.nazwa_uczelni)

    class Meta:
        verbose_name_plural = "Uczelnie"


class Wydziały(models.Model):
    id_wydzialu = models.AutoField(primary_key=True)
    nazwa_wydzialu = models.CharField(max_length=100)
    id_uczelni = models.ForeignKey(Uczelnie, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Wydziały"

    def get_uczelnia(self):
        return Uczelnie.objects.all().get(pk=self.id_uczelni.pk)

    def __str__(self):
        return str(self.id_uczelni) + ": " + str(self.id_wydzialu) + ": Nazwa: " + str(self.nazwa_wydzialu)


class Kierunki(models.Model):
    id_kierunku = models.AutoField(primary_key=True)
    nazwa_kierunku = models.CharField(max_length=100)
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)

    def get_wydzial(self):
        return Wydziały.objects.all().get(pk=self.id_wydzialu.pk)

    class Meta:
        verbose_name_plural = "Kierunki"

    def __str__(self):
        return str(self.id_wydzialu) + ": " + str(self.id_kierunku) + ": Nazwa: " + str(self.nazwa_kierunku)


class Semestry(models.Model):
    id_kierunku = models.ForeignKey(Kierunki, on_delete=models.CASCADE)
    id_semestru = models.AutoField(primary_key=True)
    nr_semestru = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name_plural = "Semestry"

    def get_kierunek(self):
        return Kierunki.objects.all().get(pk=self.id_kierunku.pk)

    def get_przedmioty(self):
        return PrzedmiotyWSemestrze.objects.all().filter(id_semestru=self)

    def __str__(self):
        return str(self.id_kierunku) + ": " + str(self.id_semestru) + ": NR: " + str(self.nr_semestru)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    class Meta:
        db_table = 'plan_user'


class Osoby(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pesel_validator = RegexValidator(r'^\d{11}')
    pesel = models.CharField(unique=True, max_length=11, validators=[pesel_validator])
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)

    class Meta:
        abstract = True
        verbose_name_plural = "Osoby"

    def __str__(self):
        return str(self.imie) + " " + str(self.nazwisko)


class Studenci(Osoby):
    class Meta:
        verbose_name_plural = "Studenci"


class Nauczyciele(Osoby):
    class Meta:
        verbose_name_plural = "Nauczyciele"


class Sale(models.Model):
    id_sali = models.AutoField(primary_key=True)
    nr_sali = models.CharField(max_length=10)
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['nr_sali', 'id_wydzialu']
        verbose_name_plural = "Sale"

    def __str__(self):
        return str(self.id_wydzialu) + ": " + str(self.nr_sali)


class ZajetoscSal(models.Model):
    id_sali = models.ForeignKey(Sale, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()

    class Meta:
        unique_together = ['id_sali', 'data_rozpoczecia', 'data_zakonczenia']
        verbose_name_plural = "ZajetoscSal"

    def get_plans(self):
        return PlanyZajecNauczycieli.objects.all().get(id_sali=self), PlanyZajecStudentow.objects.all().get(id_sali=self)


class Plany(models.Model):
    id_planu = models.AutoField(primary_key=True)
    id_semestru = models.ForeignKey(Semestry, on_delete=models.CASCADE)
    ObowiazujeOd = models.DateField()
    ObowiazujeDo = models.DateField()

    class Meta:
        abstract = True
        verbose_name_plural = "Plany"

    def is_current(self):
        now = datetime.date.today()
        return self.ObowiazujeOd <= now <= self.ObowiazujeDo


class PlanyStudentow(Plany):
    nr_albumu = models.ForeignKey(Studenci, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "PlanyStudentow"


class PlanyNauczycieli(Plany):
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "PlanyNauczycieli"


class Przedmioty(models.Model):
    id_przedmiotu = models.AutoField(primary_key=True)
    nazwa_przedmiotu = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Przedmioty"

    def __str__(self):
        return str(self.nazwa_przedmiotu)


class PrzedmiotyNauczycieli(models.Model):
    id_przedmiotu = models.ForeignKey(Przedmioty, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "PrzedmiotyNauczycieli"


class PrzedmiotyWSemestrze(models.Model):
    id_przedmiotu = models.ForeignKey(Przedmioty, on_delete=models.CASCADE)
    id_semestru = models.ForeignKey(Semestry, on_delete=models.CASCADE)
    liczba_ECTS = models.IntegerField(
        validators=[
            MaxValueValidator(30),
            MinValueValidator(0)
        ]
    )

    class Meta:
        unique_together = ['id_przedmiotu', 'id_semestru']
        verbose_name_plural = "PrzedmiotyWSemestrze"


class MiejscaZatrudnienia(models.Model):
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_wydzialu', 'id_nauczyciela']
        verbose_name_plural = "MiejscaZatrudnienia"


class PlanyZajecUzytkownikow(models.Model):
    WYKLAD = 'W'
    CWICZENIA = 'C'
    PRACOWNIASPECJALISTYCZNA = 'PS'
    LABORATORIUM = 'L'
    SEMINARIUM = 'S'
    KONSULTACJE = 'K'

    id_przedmiotu = models.ForeignKey(Przedmioty, on_delete=models.CASCADE)
    id_sali = models.ForeignKey(ZajetoscSal, on_delete=models.CASCADE)
    typ_zajec = models.CharField(max_length=2,
                                 choices=[
                                     (WYKLAD, 'Wykład'),
                                     (CWICZENIA, 'Ćwiczenia'),
                                     (PRACOWNIASPECJALISTYCZNA, 'Pracownia_specjalistyczna'),
                                     (LABORATORIUM, 'Laboratiorium'),
                                     (SEMINARIUM, 'Seminarium'),
                                     (KONSULTACJE, 'Konsultacje')
                                 ]
                                 )
    nr_grupy = models.IntegerField()

    class Meta:
        abstract = True
        verbose_name_plural = "PlanyZajecUzytkownikow"

    unique_together = ['id_planu', 'id_przedmiotu', 'id_nauczyciela', 'id_sali']


class PlanyZajecStudentow(PlanyZajecUzytkownikow):
    id_planu = models.ForeignKey(PlanyStudentow, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_planu', 'id_przedmiotu', 'id_nauczyciela', 'id_sali']
        verbose_name_plural = "PlanyZajecStudentow"


class PlanyZajecNauczycieli(PlanyZajecUzytkownikow):
    id_planu = models.ForeignKey(PlanyNauczycieli, on_delete=models.CASCADE)
    plan_studentow = models.ForeignKey(PlanyZajecStudentow, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_planu', 'id_przedmiotu', 'id_sali']
        verbose_name_plural = "PlanyZajecNauczycieli"


class StudentKierunekSemestr(models.Model):
    id_studenta = models.ForeignKey(Studenci, on_delete=models.CASCADE)
    id_semestru = models.ForeignKey(Semestry, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()

    class Meta:
        verbose_name_plural = "StudentKierunekSemestr"

    def is_current(self):
        now = datetime.date.today()
        return self.data_rozpoczecia <= now <= self.data_zakonczenia

