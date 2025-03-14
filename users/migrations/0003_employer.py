# Generated by Django 5.1.1 on 2024-09-09 10:07

import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_groups_remove_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('test', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=('users.user',),
            managers=[
                ('employer', django.db.models.manager.Manager()),
            ],
        ),
    ]
