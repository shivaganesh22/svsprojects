# Generated by Django 4.2 on 2023-04-20 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_video_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.quizes'),
        ),
    ]
