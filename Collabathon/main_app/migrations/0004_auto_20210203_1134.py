# Generated by Django 3.1.5 on 2021-02-03 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210202_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
