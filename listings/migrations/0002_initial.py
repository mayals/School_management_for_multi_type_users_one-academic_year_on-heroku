# Generated by Django 3.2.7 on 2021-12-26 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listings', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.teacher', verbose_name='Salary of Teacher'),
        ),
        migrations.AddField(
            model_name='mark',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks_created_by', to='users.teacher'),
        ),
        migrations.AddField(
            model_name='mark',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mark_set', to='users.student'),
        ),
        migrations.AddField(
            model_name='mark',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks_sub', to='listings.subject'),
        ),
        migrations.AddField(
            model_name='gradeattendance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.teacher'),
        ),
        migrations.AddField(
            model_name='gradeattendance',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.grade'),
        ),
        migrations.AddField(
            model_name='gradeattendance',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, to='users.Student', verbose_name='list of students'),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('title', 'grade')},
        ),
        migrations.AlterUniqueTogether(
            name='mark',
            unique_together={('exam_name', 'subject', 'student')},
        ),
    ]