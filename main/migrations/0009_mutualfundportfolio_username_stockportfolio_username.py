# Generated by Django 4.0.2 on 2022-03-24 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='mutualfundportfolio',
            name='username',
            field=models.ForeignKey(default=5, max_length=100, on_delete=django.db.models.deletion.CASCADE, to='main.userregistration'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockportfolio',
            name='username',
            field=models.ForeignKey(default='', max_length=100, on_delete=django.db.models.deletion.CASCADE, to='main.userregistration'),
            preserve_default=False,
        ),
    ]
