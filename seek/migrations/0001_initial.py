# Generated by Django 3.1.12 on 2025-01-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('published_date', models.DateField()),
                ('genre', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
