# Generated by Django 4.2.11 on 2024-05-24 10:22

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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('positions', models.CharField(default='["Pro", "Against"]', max_length=1000)),
                ('pos_votes', models.TextField(default=[])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.CharField(default='Pro', max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('downvote', models.ManyToManyField(blank=True, related_name='comment_downvotes', to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='website.comment')),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.post')),
                ('upvote', models.ManyToManyField(blank=True, related_name='comment_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, null=True, upload_to='attachments/')),
                ('video', models.FileField(default=None, null=True, upload_to='attachments/')),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='website.post')),
            ],
        ),
    ]
