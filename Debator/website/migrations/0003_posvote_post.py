# Generated by Django 4.2.11 on 2024-05-27 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_post_pos_votes_posvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='posvote',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.post'),
            preserve_default=False,
        ),
    ]
