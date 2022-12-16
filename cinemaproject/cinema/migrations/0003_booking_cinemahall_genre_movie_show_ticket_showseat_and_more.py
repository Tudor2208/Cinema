# Generated by Django 4.1.2 on 2022-12-16 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0002_message_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_of_seats', models.IntegerField()),
                ('booking_time', models.TimeField()),
                ('total_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CinemaHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_of_seats', models.IntegerField()),
                ('accept_4DX', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('duration', models.IntegerField()),
                ('director', models.CharField(max_length=200)),
                ('release_date', models.DateField()),
                ('description', models.TextField(max_length=1000)),
                ('genre', models.ManyToManyField(to='cinema.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('view_mode', models.CharField(max_length=45)),
                ('cinema_hall_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.cinemahall')),
                ('movie_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShowSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_nr', models.IntegerField()),
                ('booked', models.BooleanField()),
                ('booking_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.booking')),
                ('show_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.show')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.FloatField()),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='show_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.show'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
