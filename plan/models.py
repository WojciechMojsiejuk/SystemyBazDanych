from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Uczelnie(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)
    adres_uczelni = models.TextField()


class Wydziały(models.Model):
    id_wydzialu = models.AutoField(primary_key=True)
    nazwa_wydzialu = models.CharField(max_length=100)
    nazwa_uczelni = models.ForeignKey(Uczelnie, on_delete=models.CASCADE)


class Kierunki(models.Model):
    id_kierunku = models.AutoField(primary_key=True)
    nazwa_kierunku = models.CharField(max_length=100)
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)


class Semestry(models.Model):
    id_semestru = models.AutoField(primary_key=True)
    nr_semestru = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )


class Osoby(models.Model):
    pesel = models.IntegerField(validators=[
                                    MaxValueValidator(99999999999),
                                    MinValueValidator(10000000000)
                                ],
                                unique=True
                                )
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    haslo = models.CharField(max_length=50)
    czy_aktywny = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Studenci(Osoby):
    nr_albumu = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'nr_albumu'
    #REQUIRED_FIELDS = []


class Nauczyciele(Osoby):
    id_nauczyciela = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'id_nauczyciela'


class Sale(models.Model):
    id_sali = models.AutoField(primary_key=True)
    nr_sali = models.CharField(max_length=10)
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['nr_sali', 'id_wydzialu']


class ZajetoscSal(models.Model):
    id_sali = models.ForeignKey(Sale, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()

    class Meta:
        unique_together = ['id_sali', 'data_rozpoczecia', 'data_zakonczenia']


class Plany(models.Model):
    id_planu = models.AutoField(primary_key=True)
    ObowiazujeOd = models.DateField()
    ObowiazujeDo = models.DateField()

    class Meta:
        abstract = True


class PlanyStudentow(Plany):
    nr_albumu = models.ForeignKey(Studenci, on_delete=models.CASCADE)


class PlanyNauczycieli(Plany):
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)


class Przedmioty(models.Model):
    id_przedmiotu = models.AutoField(primary_key=True)
    nazwa_przedmiotu = models.CharField(max_length=50)


class PrzedmiotyNauczycieli(models.Model):
    id_przedmiotu = models.ForeignKey(Przedmioty, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)


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


class MiejscaZatrudnienia(models.Model):
    id_wydzialu = models.ForeignKey(Wydziały, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_wydzialu', 'id_nauczyciela']


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

    unique_together = ['id_planu', 'id_przedmiotu', 'id_nauczyciela', 'id_sali']


class PlanyZajecStudentow(PlanyZajecUzytkownikow):
    id_planu = models.ForeignKey(PlanyStudentow, on_delete=models.CASCADE)
    id_nauczyciela = models.ForeignKey(Nauczyciele, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_planu', 'id_przedmiotu', 'id_nauczyciela', 'id_sali']


class PlanyZajecNauczycieli(PlanyZajecUzytkownikow):
    id_planu = models.ForeignKey(PlanyNauczycieli, on_delete=models.CASCADE)
    plan_studentow = models.ForeignKey(PlanyZajecStudentow, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_planu', 'id_przedmiotu', 'id_sali']


class StudentKierunekSemestr(models.Model):
    nr_albumu = models.ForeignKey(Studenci, on_delete=models.CASCADE)
    id_kierunku = models.ForeignKey(Kierunki, on_delete=models.CASCADE)
    id_semestru = models.ForeignKey(Semestry, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
