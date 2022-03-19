# Generated by Django 4.0.1 on 2022-03-19 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('username', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('mobile', models.BigIntegerField()),
                ('category', models.CharField(blank=True, choices=[('hdr', 'hdr'), ('beauty', 'beauty'), ('bokeh', 'bokeh'), ('light', 'light')], default='hdr', max_length=30)),
                ('password', models.CharField(max_length=255)),
                ('profilepic', models.ImageField(default='profilepics\\defaultpicimg.png', upload_to='profilepics/')),
                ('bio', models.TextField(blank=True)),
                ('assign', models.CharField(blank=True, choices=[('False', 'False'), ('True', 'True')], default='False', max_length=10)),
                ('assignments_done', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]
