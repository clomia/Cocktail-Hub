# Generated by Django 3.2.5 on 2021-10-12 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archives', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='flavortag',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flavor_tags', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='constituent',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constituents', to=settings.AUTH_USER_MODEL),
        ),
    ]
