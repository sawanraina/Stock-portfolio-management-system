# Generated by Django 4.0.2 on 2022-04-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_mutualfundportfolio_username_stockportfolio_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phoneno', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=1000)),
            ],
        ),
    ]
