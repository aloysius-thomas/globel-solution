# Generated by Django 3.1.5 on 2021-01-31 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0010_auto_20210130_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]