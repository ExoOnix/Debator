# Generated by Django 4.2.11 on 2024-05-24 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_delete_reaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='positions',
            field=models.CharField(default='["Pro", "Against"]', max_length=200),
        ),
    ]