# Generated by Django 2.2.5 on 2019-11-14 10:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kierunki',
            fields=[
                ('id_kierunku', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_kierunku', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nauczyciele',
            fields=[
                ('pesel', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999999), django.core.validators.MinValueValidator(10000000000)])),
                ('imie', models.CharField(max_length=100)),
                ('nazwisko', models.CharField(max_length=100)),
                ('haslo', models.CharField(max_length=50)),
                ('czy_aktywny', models.BooleanField(default=True)),
                ('id_nauczyciela', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlanyNauczycieli',
            fields=[
                ('id_planu', models.AutoField(primary_key=True, serialize=False)),
                ('ObowiazujeOd', models.DateField()),
                ('ObowiazujeDo', models.DateField()),
                ('id_nauczyciela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Nauczyciele')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlanyStudentow',
            fields=[
                ('id_planu', models.AutoField(primary_key=True, serialize=False)),
                ('ObowiazujeOd', models.DateField()),
                ('ObowiazujeDo', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Przedmioty',
            fields=[
                ('id_przedmiotu', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_przedmiotu', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id_sali', models.AutoField(primary_key=True, serialize=False)),
                ('nr_sali', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Semestry',
            fields=[
                ('id_semestru', models.AutoField(primary_key=True, serialize=False)),
                ('nr_semestru', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Studenci',
            fields=[
                ('pesel', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999999), django.core.validators.MinValueValidator(10000000000)])),
                ('imie', models.CharField(max_length=100)),
                ('nazwisko', models.CharField(max_length=100)),
                ('haslo', models.CharField(max_length=50)),
                ('czy_aktywny', models.BooleanField(default=True)),
                ('nr_albumu', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Uczelnie',
            fields=[
                ('nazwa', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('adres_uczelni', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ZajetoscSal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_rozpoczecia', models.DateTimeField()),
                ('data_zakonczenia', models.DateTimeField()),
                ('id_sali', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Sale')),
            ],
            options={
                'unique_together': {('id_sali', 'data_rozpoczecia', 'data_zakonczenia')},
            },
        ),
        migrations.CreateModel(
            name='Wydziały',
            fields=[
                ('id_wydzialu', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_wydzialu', models.CharField(max_length=100)),
                ('nazwa_uczelni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Uczelnie')),
            ],
        ),
        migrations.CreateModel(
            name='StudentKierunekSemestr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_rozpoczecia', models.DateField()),
                ('data_zakonczenia', models.DateField()),
                ('id_kierunku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Kierunki')),
                ('id_semestru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Semestry')),
                ('nr_albumu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Studenci')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='id_wydzialu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Wydziały'),
        ),
        migrations.CreateModel(
            name='PrzedmiotyNauczycieli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_nauczyciela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Nauczyciele')),
                ('id_przedmiotu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Przedmioty')),
            ],
        ),
        migrations.CreateModel(
            name='PlanyZajecStudentow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ_zajec', models.CharField(choices=[('W', 'Wykład'), ('C', 'Ćwiczenia'), ('PS', 'Pracownia_specjalistyczna'), ('L', 'Laboratiorium'), ('S', 'Seminarium'), ('K', 'Konsultacje')], max_length=2)),
                ('nr_grupy', models.IntegerField()),
                ('id_nauczyciela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Nauczyciele')),
                ('id_planu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.PlanyStudentow')),
                ('id_przedmiotu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Przedmioty')),
                ('id_sali', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.ZajetoscSal')),
            ],
            options={
                'unique_together': {('id_planu', 'id_przedmiotu', 'id_nauczyciela', 'id_sali')},
            },
        ),
        migrations.AddField(
            model_name='planystudentow',
            name='nr_albumu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Studenci'),
        ),
        migrations.AddField(
            model_name='kierunki',
            name='id_wydzialu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Wydziały'),
        ),
        migrations.AlterUniqueTogether(
            name='sale',
            unique_together={('nr_sali', 'id_wydzialu')},
        ),
        migrations.CreateModel(
            name='PrzedmiotyWSemestrze',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liczba_ECTS', models.IntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)])),
                ('id_przedmiotu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Przedmioty')),
                ('id_semestru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Semestry')),
            ],
            options={
                'unique_together': {('id_przedmiotu', 'id_semestru')},
            },
        ),
        migrations.CreateModel(
            name='PlanyZajecNauczycieli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ_zajec', models.CharField(choices=[('W', 'Wykład'), ('C', 'Ćwiczenia'), ('PS', 'Pracownia_specjalistyczna'), ('L', 'Laboratiorium'), ('S', 'Seminarium'), ('K', 'Konsultacje')], max_length=2)),
                ('nr_grupy', models.IntegerField()),
                ('id_planu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.PlanyNauczycieli')),
                ('id_przedmiotu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Przedmioty')),
                ('id_sali', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.ZajetoscSal')),
                ('plan_studentow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.PlanyZajecStudentow')),
            ],
            options={
                'unique_together': {('id_planu', 'id_przedmiotu', 'id_sali')},
            },
        ),
        migrations.CreateModel(
            name='MiejscaZatrudnienia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_nauczyciela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Nauczyciele')),
                ('id_wydzialu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.Wydziały')),
            ],
            options={
                'unique_together': {('id_wydzialu', 'id_nauczyciela')},
            },
        ),
    ]
