# Generated by Django 5.0.1 on 2024-02-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblogs', '0004_contact_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]