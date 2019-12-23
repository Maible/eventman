# Generated by Django 3.0.1 on 2019-12-23 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Short description')),
                ('long_description', models.TextField(blank=True, null=True, verbose_name='Long description')),
                ('capacity', models.IntegerField(default=10, verbose_name='Capacity')),
                ('guest_per_person', models.IntegerField(default=0, verbose_name='Allowed guests')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='EventInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts_at', models.DateTimeField(verbose_name='Start time')),
                ('ends_at', models.DateTimeField(verbose_name='End time')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='event.Event')),
            ],
            options={
                'verbose_name': 'Event interval',
                'verbose_name_plural': 'Event intervals',
                'ordering': ('event', 'starts_at'),
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('address_first', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address 1')),
                ('address_second', models.CharField(max_length=100, verbose_name='Address 2')),
                ('max_capacity', models.IntegerField(default=10, verbose_name='Maximum capacity')),
            ],
            options={
                'verbose_name': 'Venue',
                'verbose_name_plural': 'Venues',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EventInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Accepted'), (2, 'Partially attending'), (3, 'Declined')], default=0, verbose_name='Attendance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='event.Event')),
                ('interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.EventInterval')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event invitation',
                'verbose_name_plural': 'Event invitations',
                'ordering': ('event', 'user'),
            },
        ),
        migrations.CreateModel(
            name='EventGuest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email address')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='event.EventInvitation')),
            ],
            options={
                'verbose_name': 'Event guest',
                'verbose_name_plural': 'Event guests',
                'ordering': ('invitation', 'created_at'),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.Venue'),
        ),
        migrations.AddConstraint(
            model_name='eventinvitation',
            constraint=models.UniqueConstraint(fields=('event', 'user'), name='unique_invitation'),
        ),
    ]
