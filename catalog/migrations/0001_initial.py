# Generated by Django 2.2.5 on 2019-09-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='testmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homecity', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
