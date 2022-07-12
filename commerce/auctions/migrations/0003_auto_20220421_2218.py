# Generated by Django 3.2.13 on 2022-04-21 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20220421_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidder',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commenter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL),
        ),
    ]
