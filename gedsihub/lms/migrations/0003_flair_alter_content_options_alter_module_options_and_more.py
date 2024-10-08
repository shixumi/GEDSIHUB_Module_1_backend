# Generated by Django 5.0.7 on 2024-08-09 07:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_remove_course_instructor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['position']},
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='options',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='content',
            name='content',
        ),
        migrations.RemoveField(
            model_name='content',
            name='order',
        ),
        migrations.RemoveField(
            model_name='module',
            name='order',
        ),
        migrations.AddField(
            model_name='assessment',
            name='passing_grade',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='questions',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='title',
            field=models.CharField(default='Module', max_length=255),
        ),
        migrations.AddField(
            model_name='content',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='position',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='text_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='position',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='module',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assessment', to='lms.module'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('text', 'Text'), ('video', 'Video'), ('image', 'Image')], max_length=10),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='lms.course'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='progress',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='lms.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flairs', models.ManyToManyField(related_name='forums', to='lms.flair')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums', to='lms.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='lms.forum')),
            ],
        ),
    ]
