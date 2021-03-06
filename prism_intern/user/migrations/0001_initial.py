# Generated by Django 4.0.1 on 2022-03-27 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('mobile', models.BigIntegerField()),
                ('profilepic', models.ImageField(default='profilepics\\defaultpicimg.png', upload_to='profilepics/')),
                ('bio', models.TextField(blank=True, default='')),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
