# Generated by Django 5.1.6 on 2025-02-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_full_name_user_usn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='credit_points',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='grade',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='grade_points',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='marks',
            field=models.FloatField(),
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together={('student', 'semester', 'course')},
        ),
    ]
