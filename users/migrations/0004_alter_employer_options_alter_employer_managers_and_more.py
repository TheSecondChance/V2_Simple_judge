# Generated by Django 5.1.1 on 2024-09-09 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0003_employer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employer',
            options={'verbose_name': 'Employer', 'verbose_name_plural': 'Employers'},
        ),
        migrations.AlterModelManagers(
            name='employer',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='employer',
            old_name='test',
            new_name='payment',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
