# Generated by Django 3.2.7 on 2021-12-26 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('listings', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gradeattendance',
            options={'ordering': ['-created_by']},
        ),
        migrations.RenameField(
            model_name='gradeattendance',
            old_name='Att_date',
            new_name='att_date',
        ),
        migrations.AlterField(
            model_name='gradeattendance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='att_author', to='users.teacher'),
        ),
    ]