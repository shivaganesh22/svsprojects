# Generated by Django 4.2 on 2023-04-19 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=50)),
                ('video_url', models.URLField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.quizes')),
            ],
        ),
    ]
